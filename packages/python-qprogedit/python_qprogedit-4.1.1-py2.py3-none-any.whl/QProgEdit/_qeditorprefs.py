#-*- coding:utf-8 -*-

"""
This file is part of QProgEdit.

QProgEdit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

QProgEdit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with QProgEdit.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from qtpy import QtGui, QtCore, QtWidgets
from QProgEdit.pyqt5compat import Qsci
from QProgEdit.py3compat import *
from QProgEdit import QColorScheme
from QProgEdit import QUiLoader

class QEditorPrefs(QtWidgets.QWidget, QUiLoader):

	"""
	desc:
		An editor preferences widget.
	"""

	# These options correspond to the names of checkboxes in the prefsWidget
	# UI definition.
	checkBoxCfgOptions = [u'AutoComplete', u'AutoIndent',
		u'HighlightCurrentLine', u'HighlightMatchingBrackets', u'LineNumbers',
		u'ShowEol', u'ShowFolding', u'ShowIndent', u'ShowWhitespace',
		u'WordWrap', u'Validate']

	def __init__(self, qProgEdit):

		"""
		desc:
			Constructor.

		arguments:
			qProgEdit:
				desc:	The parent QProgEdit.
				type:	QProgEdit
		"""

		super(QEditorPrefs, self).__init__(qProgEdit)
		self.qProgEdit = qProgEdit
		self.loadUi(u'prefsWidget')
		self.bestHeight = self.height()
		self.lock = False
		# Make connections
		self.ui.fontComboBoxFontFamily.activated.connect(self.apply)
		self.ui.lineEditCommentShortcut.editingFinished.connect(self.apply)
		self.ui.lineEditUncommentShortcut.editingFinished.connect(self.apply)
		self.ui.comboBoxColorScheme.activated.connect(self.apply)
		self.ui.spinBoxFontSize.valueChanged.connect(self.apply)
		self.ui.spinBoxTabWidth.valueChanged.connect(self.apply)
		self.ui.checkBoxWordWrapMarker.toggled.connect(self.apply)
		for cfg in self.checkBoxCfgOptions:
			checkBox = getattr(self.ui, 'checkBox%s' % cfg)
			checkBox.stateChanged.connect(self.apply)

	def refresh(self):

		"""
		desc:
			Refreshes the controls.
		"""

		self.lock = True
		index = self.ui.fontComboBoxFontFamily.findText(
			self.qProgEdit.cfg.qProgEditFontFamily)
		# Fill the shortcut fields
		self.ui.lineEditCommentShortcut.setText(
			self.qProgEdit.cfg.qProgEditCommentShortcut)
		self.ui.lineEditUncommentShortcut.setText(
			self.qProgEdit.cfg.qProgEditUncommentShortcut)
		# Fill the color scheme combobox and select the current color scheme
		self.ui.comboBoxColorScheme.clear()
		i = 0
		for scheme in QColorScheme.schemes:
			self.ui.comboBoxColorScheme.addItem(scheme)
			if scheme == self.qProgEdit.cfg.qProgEditColorScheme:
				self.ui.comboBoxColorScheme.setCurrentIndex(i)
			i += 1
		self.ui.fontComboBoxFontFamily.setCurrentIndex(index)
		self.ui.spinBoxFontSize.setValue(self.qProgEdit.cfg.qProgEditFontSize)
		self.ui.spinBoxTabWidth.setValue(self.qProgEdit.cfg.qProgEditTabWidth)
		self.ui.checkBoxWordWrapMarker.setChecked(
			self.qProgEdit.cfg.qProgEditWordWrapMarker)
		for cfg in self.checkBoxCfgOptions:
			checked = getattr(self.qProgEdit.cfg, u'qProgEdit%s' % cfg)
			checkBox = getattr(self.ui, u'checkBox%s' % cfg)
			checkBox.setChecked(checked)
		self.lock = False

	def apply(self, dummy=None):

		"""
		desc:
			Applies the controls.
		"""

		if self.lock:
			return
		self.qProgEdit.cfg.qProgEditFontFamily = str(
			self.ui.fontComboBoxFontFamily.currentText())
		self.qProgEdit.cfg.qProgEditColorScheme = str(
			self.ui.comboBoxColorScheme.currentText())
		self.qProgEdit.cfg.qProgEditCommentShortcut = str(
			self.ui.lineEditCommentShortcut.text())
		self.qProgEdit.cfg.qProgEditUncommentShortcut = str(
			self.ui.lineEditUncommentShortcut.text())
		self.qProgEdit.cfg.qProgEditFontSize = self.ui.spinBoxFontSize.value()
		self.qProgEdit.cfg.qProgEditTabWidth = self.ui.spinBoxTabWidth.value()
		if self.ui.checkBoxWordWrapMarker.isChecked():
			self.qProgEdit.cfg.qProgEditWordWrapMarker = 80
		else:
			self.qProgEdit.cfg.qProgEditWordWrapMarker = 0
		for cfg in self.checkBoxCfgOptions:
			checkBox = getattr(self.ui, u'checkBox%s' % cfg)
			checked = checkBox.isChecked()
			setattr(self.qProgEdit.cfg, u'qProgEdit%s' % cfg, checked)
		if self.qProgEdit.tabManager is not None:
			self.qProgEdit.tabManager.applyCfg()
		else:
			self.qProgEdit.applyCfg()
