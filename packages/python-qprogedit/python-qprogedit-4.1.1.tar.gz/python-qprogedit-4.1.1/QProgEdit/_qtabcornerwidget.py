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
from QProgEdit import QLangMenu, QEditorStatus, _

class QTabCornerWidget(QtWidgets.QWidget):

	"""
	desc:
		Contains a number of buttons that are displayed in the tab bar.
	"""

	def __init__(self, tabManager, msg=None, handlerButtonText=None,
		runButton=False):

		"""
		desc:
			Constructor.

		arguments:
			tabManager:
				desc:	A tab manager.
				type:	QTabManager

		keywords:
			msg:
				desc:	An informative text message.
				type:	[str, unicode, NoneType]
			handlerButtonText:
				desc:	Text for a top-right button, which can be clicked to
						call the handler, or None for no button.
				type:	[str, unicode, NoneType]
			runButton:
				desc:	Indicates whether a run-selected-text button should be
						shown.
				type:	bool
		"""

		super(QTabCornerWidget, self).__init__(tabManager)
		self.tabManager = tabManager
		# Run button
		if runButton:
			self.runButton = QtWidgets.QPushButton(QtGui.QIcon.fromTheme(
				u'system-run'), u'', self)
			self.runButton.setToolTip(_(u'Run selected text'))
			self.runButton.setCheckable(False)
			self.runButton.clicked.connect(self.tabManager.runSelectedText)
		# Preferences button
		self.prefsButton = QtWidgets.QPushButton(QtGui.QIcon.fromTheme(
			u'preferences-desktop'), u'', self)
		self.prefsButton.setCheckable(True)
		self.prefsButton.toggled.connect(self.tabManager.togglePrefs)
		# Find button
		self.findButton = QtWidgets.QPushButton(QtGui.QIcon.fromTheme(
			u'edit-find'), u'', self)
		self.findButton.setCheckable(True)
		self.findButton.toggled.connect(self.tabManager.toggleFind)
		# Language button (filled by update())
		self.langButton = QtWidgets.QPushButton(self)
		self.langButton.setMenu(QLangMenu(self))
		self.langShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(u'Ctrl+Shift+L'),
			self.tabManager, context=QtCore.Qt.WidgetWithChildrenShortcut)
		self.langShortcut.activated.connect(self.langButton.click)
		# Handler button
		if handlerButtonText is not None:
			self.handlerButton = QtWidgets.QPushButton(QtGui.QIcon.fromTheme(
				u'document-save'), handlerButtonText, self)
			self.handlerButton.clicked.connect(self.handlerButtonClicked)
		else:
			self.handlerButton = None
		# Editor status
		self.statusWidget = QEditorStatus(self)
		# Message
		if msg is not None:
			self.msgLabel = QtWidgets.QLabel(u'<small>%s</small>' % msg, parent= \
				self)
		self.hBox = QtWidgets.QHBoxLayout(self)
		self.hBox.setSpacing(2)
		self.hBox.setContentsMargins(2,2,2,2)
		if msg is not None:
			self.hBox.addWidget(self.msgLabel)
		self.hBox.addWidget(self.statusWidget)
		if runButton:
			self.hBox.addWidget(self.runButton)
		self.hBox.addWidget(self.prefsButton)
		self.hBox.addWidget(self.findButton)
		self.hBox.addWidget(self.langButton)
		if self.handlerButton is not None:
			self.hBox.addWidget(self.handlerButton)
		self.setLayout(self.hBox)
		# Set the tab order for keyboard navigation
		self.setTabOrder(self.prefsButton, self.findButton)
		self.setTabOrder(self.findButton, self.langButton)
		self.setTabOrder(self.langButton, self.handlerButton)

	def handlerButtonClicked(self):

		"""
		desc:
			Is called when the handler button is clicked and emits the relevant
			signals.
		"""

		self.tabManager.handlerButtonClicked.emit(
			self.tabManager.currentIndex())
		self.tabManager.tab().handlerButtonClicked.emit()

	def update(self):

		"""
		desc:
			Updates widget to reflect document contents.
		"""

		self.langButton.setIcon(QtGui.QIcon.fromTheme(
			u'text-x-%s' % self.tabManager.tab().lang().lower(),
			QtGui.QIcon.fromTheme(u'text-plain')))
		self.findButton.setChecked(False)
		self.prefsButton.setChecked(False)
