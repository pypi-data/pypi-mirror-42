# visualequation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# visualequation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

""" The module that manages the editing equation. """
import os
import types

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import eqtools
from . import eqhist
from . import conversions
from .symbols import utils
from . import eqsel
from .errors import ShowError

class SaveDialog(QDialog):

    prev_format_index = 0
    prev_size = 600.

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Save equation')
        label = QLabel(
            _("Select format:\n\nNote: Equations can only be recovered"
              " from PNG and PDF."))
        label.setWordWrap(True)
        items = ["PNG", "PDF", "EPS", "SVG"]
        self.combo = QComboBox(self)
        self.combo.addItems(items)
        self.combo.setCurrentIndex(self.prev_format_index)
        self.label_spin = QLabel(_('Size (dpi):'))
        self.spin = QDoubleSpinBox(self)
        self.spin.setMaximum(10000)
        # Just avoid negative numbers
        # Minimum conditions are set later
        self.spin.setMinimum(0.01)
        self.spin.setValue(self.prev_size)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        vbox = QVBoxLayout(self)
        vbox.addWidget(label)
        vbox.addWidget(self.combo)
        vbox.addWidget(self.label_spin)
        vbox.addWidget(self.spin)
        vbox.addWidget(self.buttons)
        self.combo.currentIndexChanged.connect(self.changed_combo)
        self.spin.valueChanged.connect(self.changed_spin)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def changed_combo(self, index):
        if "SVG" == self.combo.currentText():
            self.label_spin.setText(_('Size (scale):'))
            self.spin.setValue(5)
        else:
            self.label_spin.setText(_('Size (dpi):'))
            self.spin.setValue(600)

    def changed_spin(self):
        if "SVG" == self.combo.currentText():
            if self.spin.value() < 0.:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(
                    True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(
                    True)
        else:
            if self.spin.value() < 10.:
                self.buttons.button(QDialogButtonBox.Ok).setDisabled(
                    True)
            else:
                self.buttons.button(QDialogButtonBox.Ok).setEnabled(
                    True)

    @staticmethod
    def get_save_options(parent=None):
        dialog = SaveDialog(parent)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            SaveDialog.prev_format_index = dialog.combo.currentIndex()
            SaveDialog.prev_size = dialog.spin.value()
            return ((dialog.combo.currentText(),
                     dialog.spin.value()),
                    True)
        else:
            return ((None, None), False)

class Eq:
    def __init__(self, temp_dir, setPixmap, parent):

        init_eq = [utils.NEWARG]
        self.eq_buffer = []
        self.eq = list(init_eq) # It will be mutated by the replace functions
        self.temp_dir = temp_dir
        self.parent = parent
        self.eqsel = eqsel.Selection(init_eq, 0, temp_dir, setPixmap)
        self.eqsel.display(self.eq)
        self.eqhist = eqhist.EqHist(self.eqsel)

    def insert(self, oper):
        """
        Insert a symbol next to selection by Juxt and, if it is an operator,
        set all the arguments to NewArg.
        """
        def replace_op_in_eq(op):
            """
            Given an operator, it is replaced in self.eq according to
            the rules of above. It also modify self.eqsel.index to point to
            the smartest block.
            """            
            if isinstance(op, str):
                if self.eq[self.eqsel.index] == utils.NEWARG:
                    self.eq[self.eqsel.index] = op
                else:
                    if self.eqsel.right:
                        self.eqsel.index = eqtools.insertrbyJUXT(
                            self.eq, self.eqsel.index, [op])
                    else:
                        self.eqsel.index = eqtools.insertlbyJUXT(
                            self.eq, self.eqsel.index, [op])
            elif isinstance(op, utils.Op):
                opeq = [op] + [utils.NEWARG]*op.n_args
                if self.eq[self.eqsel.index] == utils.NEWARG:
                    self.eq[self.eqsel.index:self.eqsel.index+1] = opeq
                else:
                    if self.eqsel.right:
                        self.eqsel.index \
                            = eqtools.insertrbyJUXT(self.eq,
                                                    self.eqsel.index,
                                                    opeq)
                    else:
                        self.eqsel.index \
                            = eqtools.insertlbyJUXT(self.eq,
                                                    self.eqsel.index,
                                                    opeq)
                # Point to the first argument, if any
                if op.n_args > 0:
                    self.eqsel.index += 1
                    
            else:
                ShowError('Unknown type of operator in insert: ' + repr(op),
                          True)

        self.eqhist.update(self.eqsel)
        if isinstance(oper, types.FunctionType):
            op = oper(self.parent)
            if op:
                replace_op_in_eq(op)
            else:
                return None
        else:
            replace_op_in_eq(oper)

        self.eqsel.display(self.eq)
        self.eqhist.save(self.eqsel)

    def insert_substituting(self, oper):
        """
        Given an operator, the equation block pointed by self.eqsel.index
        is replaced by that operator and the selection is used as follows:

        If op is a str, just replace it.

        If op is an unary operator, put the selected block as the argument
        of the operator.

        If the operator has more than one argument, put the selected block
        as the first argument of the operator. Put NewArg symbols in the
        rest of the arguments.

        If the operator has more than one argument, selection index is
        changed to the second argument of the operator because the user
        probably will want to change that argument.
        """
        def replace_op_in_eq(op):
            """
            Given an operator, it is replaced in self.eq according to
            the rules of above. It also modify self.eqsel.index to point to
            the smartest block.
            """
            if isinstance(op, str) or \
               (isinstance(op, utils.Op) and op.n_args == 0):
                eqtools.replaceby(self.eq, self.eqsel.index, [op])
            elif isinstance(op, utils.Op) and op.n_args == 1:
                self.eq.insert(self.eqsel.index, op)
            elif isinstance(op, utils.Op) and op.n_args > 1:
                index_end_arg1 = eqtools.nextblockindex(self.eq,
                                                        self.eqsel.index)
                self.eq[self.eqsel.index:index_end_arg1] = [op] \
                                    + self.eq[self.eqsel.index:index_end_arg1] \
                                    + [utils.NEWARG] * (op.n_args-1)
                self.eqsel.index = index_end_arg1+1
            else:
                ShowError('Unknown type of operator in insert_subst: '
                          + repr(op), True)

        self.eqhist.update(self.eqsel)
        if isinstance(oper, types.FunctionType):
            op = oper(self.parent)
            if op:
                replace_op_in_eq(op)
            else:
                return None
        else:
            replace_op_in_eq(oper)

        self.eqsel.display(self.eq)
        self.eqhist.save(self.eqsel)

    def insert_sup_substituting(self):
        # Blacklist some operators
        if hasattr(self.eq[self.eqsel.index], 'type_') \
           and self.eq[self.eqsel.index].type_ in utils.INDEX_BLACKLIST:
            return

        self.eqhist.update(self.eqsel)
        # If the user specifies a JUXT, they refer to the first or last element
        if self.eq[self.eqsel.index] == utils.JUXT:
            if self.eqsel.right:
                self.eqsel.index = eqtools.last_arg_of_JUXT_seq(
                    self.eq, self.eqsel.index)
            else:
                self.eqsel.index = eqtools.first_arg_of_JUXT_seq(
                    self.eq, self.eqsel.index)
        # Create a list with a index arg list
        args = eqtools.indexop2arglist(self.eq, self.eqsel.index)
        # Change it to add the new index
        if self.eqsel.right:
            up_index = 3
            if not args[up_index]:
                args[up_index] = [utils.NEWARG]
        else:
            up_index = 4
            if not args[up_index]:
                args[up_index] = [utils.NEWARG]
        elems = 0
        for i in range(up_index):
            if args[i] != None:
                elems += len(args[i])

        new_op = eqtools.arglist2indexop(args)
        # Flat the list of args
        new_args = eqtools.flat_arglist(args)
        new_block = [new_op] + new_args
        end_old_block = eqtools.nextblockindex(self.eq, self.eqsel.index) 
        self.eq[self.eqsel.index:end_old_block] = new_block

        self.eqsel.index += 1 + elems
        self.eqsel.display(self.eq)
        self.eqhist.save(self.eqsel)

    def insert_sub_substituting(self):
        # Blacklist some operators
        if hasattr(self.eq[self.eqsel.index], 'type_') \
           and self.eq[self.eqsel.index].type_ in utils.INDEX_BLACKLIST:
            return

        self.eqhist.update(self.eqsel)
        # If the user specifies a JUXT, they refer to the first or last element
        if self.eq[self.eqsel.index] == utils.JUXT:
            if self.eqsel.right:
                self.eqsel.index = eqtools.last_arg_of_JUXT_seq(self.eq,
                                                              self.eqsel.index)
            else:
                self.eqsel.index = eqtools.first_arg_of_JUXT_seq(self.eq,
                                                               self.eqsel.index)
        # Create a list with a index arg list
        args = eqtools.indexop2arglist(self.eq, self.eqsel.index)
        # Change it to add the new index
        if self.eqsel.right:
            down_index = 2
            if not args[down_index]:
                args[down_index] = [utils.NEWARG]
        else:
            down_index = 1
            if not args[down_index]:
                args[down_index] = [utils.NEWARG]
        elems = 0
        for i in range(down_index):
            if args[i] != None:
                elems += len(args[i])

        new_op = eqtools.arglist2indexop(args)
        # Flat the list of args
        new_args = eqtools.flat_arglist(args)
        new_block = [new_op] + new_args
        end_old_block = eqtools.nextblockindex(self.eq, self.eqsel.index) 
        self.eq[self.eqsel.index:end_old_block] = new_block

        self.eqsel.index += 1 + elems
        self.eqsel.display(self.eq)
        self.eqhist.save(self.eqsel)

    def remove_sel(self):
        """
        If self.eqsel.index points to the first or second arg of a Juxt,
        it removes the Juxt and leaves the other argument in its place.
        If it is a script, it removes it.
        Else, it removes the block pointed and put a NEWARG.
        """
        # Check if it is the arg of a JUXT and leave it clean
        cond_arg_JUXT, JUXT_index, other_arg_index = eqtools.is_arg_of_JUXT(
            self.eq, self.eqsel.index)
        if cond_arg_JUXT:
            self.eqhist.update(self.eqsel)
            JUXT_end = eqtools.nextblockindex(self.eq, JUXT_index)
            # If eqsel.index is the first argument (instead of the second)
            if JUXT_index + 1 == self.eqsel.index:
                self.eq[JUXT_index:JUXT_end] = self.eq[
                    other_arg_index:JUXT_end]
            else:
                self.eq[JUXT_index:JUXT_end] = self.eq[
                    other_arg_index:self.eqsel.index]
            self.eqsel.index = JUXT_index
            self.eqsel.set_valid_index(self.eq)
        else:
            # If it is a script, downgrade the script operator
            cond_script, script_op_index, arg_pos = eqtools.is_script(
                self.eq, self.eqsel.index)
            if cond_script:
                self.eqhist.update(self.eqsel)
                args = eqtools.indexop2arglist(self.eq, script_op_index)
                # Find which element of the list has to be removed
                arg_index = 0
                for index, arg in enumerate(args):
                    if arg is not None:
                        if arg_index == arg_pos:
                            args[index] = None
                            break
                        else:
                            arg_index += 1
                new_op = eqtools.arglist2indexop(args)
                end_block = eqtools.nextblockindex(self.eq, script_op_index)
                if new_op is None:
                    self.eq[script_op_index:end_block] = args[0]
                else:
                    new_args = eqtools.flat_arglist(args)
                    self.eq[script_op_index:end_block] = [new_op] + new_args
                self.eqsel.index = script_op_index
            elif self.eq[self.eqsel.index] != utils.NEWARG:
                self.eqhist.update(self.eqsel)
                eqtools.replaceby(self.eq, self.eqsel.index, [utils.NEWARG])
            else:
                # Avoid displaying and saving in history if nothing to do
                return

        self.eqsel.display(self.eq)
        self.eqhist.save(self.eqsel)

    def new_eq(self):
        self.eq = [utils.NEWARG]
        self.eqsel.index = 0
        self.eqsel.display(self.eq)
        self.eqhist = eqhist.EqHist(self.eqsel)
        
    def open_eq(self, filename=None):
        neweq = conversions.open_eq(self.parent, filename)
        if neweq != None:
            self.eq = list(neweq)
            self.eqsel.index = 0
            self.eqsel.display(self.eq)
            self.eqhist.save(self.eqsel)

    def save_eq(self):
        (save_format, size), ok = SaveDialog.get_save_options(self.parent)
        if not ok:
            return
        # Implement a Save File dialog
        # The staticmethod does not accept default suffix
        formatfilter = save_format + " (*." + save_format.lower() + ")"
        dialog = QFileDialog(self.parent, 'Save equation', '', formatfilter)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDefaultSuffix(save_format.lower())
        dialog.setOption(QFileDialog.DontConfirmOverwrite, True)
        if not dialog.exec_():
            return
        filename = dialog.selectedFiles()[0]
        # Implement an Overwrite? dialog since the default one does not
        # check filename when default suffix extension has to be added
        if os.path.exists(filename):
            msg = _('A file named "%s" already exists. Do you want to'
            ' replace it?') % os.path.basename(filename) 
            ret_val = QMessageBox.question(self.parent, _('Overwrite'), msg)
            if ret_val != QMessageBox.Yes:
                return
        if save_format == 'PNG':
            conversions.eq2png(self.eq, dpi=size, bg=None,
                               directory=self.temp_dir, png_fpath=filename,
                               add_metadata=True)
        elif save_format == 'PDF':
            conversions.eq2pdf(self.eq, size, self.temp_dir, filename)
        elif save_format == 'SVG':
            conversions.eq2svg(self.eq, size, self.temp_dir, filename)
        elif save_format == 'EPS':
            conversions.eq2eps(self.eq, size, self.temp_dir, filename)

    def recover_prev_eq(self):
        """ Recover previous equation from the historial, if any """
        preveq, self.eqsel.index, self.eqsel.right = self.eqhist.get_prev()
        self.eq = list(preveq)
        self.eqsel.display(self.eq, self.eqsel.right)

    def recover_next_eq(self):
        """ Recover next equation from the historial, if any """
        nexteq, self.eqsel.index, self.eqsel.right = self.eqhist.get_next()
        self.eq = list(nexteq)
        self.eqsel.display(self.eq, self.eqsel.right)

    def sel2eqbuffer(self):
        """ Copy block pointed by self.eqsel.index to self.eq_buffer """
        end_sel_index = eqtools.nextblockindex(self.eq, self.eqsel.index)
        self.eq_buffer = self.eq[self.eqsel.index:end_sel_index]

    def eqbuffer2sel(self):
        """
        Append self.eq_buffer to the right of the block pointed by
        self.eqsel.index. If the block is a NEWARG, just replace it.
        """
        if self.eq_buffer != []:
            if self.eq[self.eqsel.index] == utils.NEWARG:
                self.eq[self.eqsel.index:self.eqsel.index+1] = self.eq_buffer
            else:
                if self.eqsel.right:
                    self.eqsel.index = eqtools.insertrbyJUXT(self.eq,
                                                           self.eqsel.index,
                                                           self.eq_buffer)
                else:
                    self.eqsel.index = eqtools.insertlbyJUXT(self.eq,
                                                           self.eqsel.index,
                                                           self.eq_buffer)
            self.eqsel.display(self.eq)
            self.eqhist.save(self.eqsel)
