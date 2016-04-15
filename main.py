import random, os, time

from PySide import QtGui, QtCore

from config import settings

factors = [
	{
		"name": "Mental Demand",
		"description": '''
			How much mental and perceptual activity was required?
			Was the task easy or demanding, simple or complex?'''
	},{
		"name": "Physical Demand",
		"description": '''
			How much physical activity was required?
			Was the task easy or demanding, slack or strenuous?'''
	},{
		"name": "Temporal Demand",
		"description": '''
			How much time pressure did you feel due to the pace at which
			the tasks or task elements occurred? Was the pace slow or rapid?'''
	},{
		"name": "Performance",
		"description": '''
			How successful were you in performing the task?
			How satisfied were you with your performance?'''
	},{
		"name": "Frustration",
		"description": '''
			How irritated, stressed, and annoyed versus
			content, relaxed, and complacent did you feel during the task?'''
	},{
		"name": "Effort",
		"description": '''
			How hard did you have to work (mentally and physically)
			to accomplish your level of performance?'''
	},
]

class DemandSlider(QtGui.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setLayout(QtGui.QVBoxLayout())
		
		self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slider.setRange(0, 20)
		self.slider.setTickInterval(1)
		self.slider.setValue(11)
		self.slider.setTickPosition(QtGui.QSlider.TicksBothSides)
		
		self.layout().addWidget(self.slider)
		
		labels = QtGui.QWidget(self)
		labels.setLayout(QtGui.QHBoxLayout())
		labels.layout().addWidget(QtGui.QLabel('Low'))
		label = QtGui.QLabel('High')
		label.setAlignment(QtCore.Qt.AlignRight)
		labels.layout().addWidget(label)
		self.layout().addWidget(labels)
		
	def value(self):
		return self.slider.value() * 5

class ComparisonPage(QtGui.QWidget):
	chosen = QtCore.Signal(str, object)
	cleared = QtCore.Signal(object)

	def __init__(self, options):
		super().__init__()
		instructions = QtGui.QLabel('<font size="8">Select the Scale Title that represents the more important contributor to workload for the specific task you performed in this experiment.</font>')
		instructions.setWordWrap(True)
		instructions.setAlignment(QtCore.Qt.AlignCenter)
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().setAlignment(QtCore.Qt.AlignVCenter)
		self.layout().addWidget(instructions)
		
		buttonGrid = QtGui.QHBoxLayout()
		self.options = options
		self.buttons = []
		for column, option in enumerate(self.options):
			b = QtGui.QToolButton()
			b.setText(option['name'])
			b.setCheckable(True)
			b.clicked.connect(self.onChoose)
			b.setAutoExclusive(True)
			b.setMinimumHeight(200)
			b.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
			b.setToolTip(option['description'].strip().replace('\t', ''))
			self.buttons.append(b)
			buttonGrid.addWidget(b)
		self.layout().addLayout(buttonGrid)
			
	def getChoice(self):
		for b in self.buttons:
			if b.isChecked():
				return b.text()

	def onChoose(self):
		for b in self.buttons:
			if b.isChecked():
				self.chosen.emit(b.text(), self.options)
				return
		self.cleared.emit(self.options)
		
class TLXWindow(QtGui.QWidget):
	def __init__(self):
		super().__init__()
		self.startTime = None
		
		self.setWindowTitle('NASA TLX')
		font = self.font()
		font.setPointSize(14)
		self.setFont(font)
		self.setLayout(QtGui.QVBoxLayout())
		
		self.createTabs()
		self.createNavigation()
		
	def createTabs(self):
		self.tabs = QtGui.QTabWidget(self)
		self.tabs.tabBar().hide()
		
		self.createParticipantPage()
		self.createFactorsPage()
		self.createComparisonPages()
		self.createFinalPage()
		self.layout().addWidget(self.tabs)
		
	def createNavigation(self):
		container = QtGui.QWidget(self)
		container.setLayout(QtGui.QHBoxLayout())
		
		self.previousButton = QtGui.QPushButton(' Previous')
		self.previousButton.clicked.connect(self.gotoPreviousPage)
		self.previousButton.setDisabled(True)
		container.layout().addWidget(self.previousButton)
		
		container.layout().addWidget(QtGui.QLabel(''))
		container.layout().addWidget(QtGui.QLabel(''))
		
		self.nextButton = QtGui.QPushButton('Next ')
		self.nextButton.clicked.connect(self.gotoNextPage)
		container.layout().addWidget(self.nextButton)
		
		self.layout().addWidget(container)
		
	def createParticipantPage(self):
		container = QtGui.QWidget()
		container.setLayout(QtGui.QVBoxLayout())
		container.layout().setAlignment(QtCore.Qt.AlignVCenter)
		container.layout().addWidget(QtGui.QLabel('<b>Participant ID</b>'))
		self.participantID = QtGui.QLineEdit()
		container.layout().addWidget(self.participantID)
		
		self.tabs.addTab(container, 'Participant Info')
		
	def createFactorsPage(self):
		w = QtGui.QWidget()
		layout = QtGui.QFormLayout()
		self.sliders = {}
		for f in factors:
			slider = DemandSlider()
			layout.addRow('<br><b>%s</b>' % f['name'], None)
			description = '<i>%s</i>' % f['description'].strip().replace('\n', '<br>')
			layout.addRow(description, slider)
			
			self.sliders[f['name']] = slider
			
		w.setLayout(layout)
		self.tabs.addTab(w, 'Factors')
		
	def createComparisonPages(self):
		self.comparisonPages = []
		comparisons = []

		for i, f1 in enumerate(factors):
			for j in range(i+1, len(factors)):
				f2 = factors[j]
				pair = [f1, f2]
				random.shuffle(pair)
				comparisons.append(pair)
				
		random.shuffle(comparisons)
		for c in comparisons:
			page = ComparisonPage(c)
			self.tabs.addTab(page, '%s vs %s' % (c[0], c[1]))
			page.chosen.connect(self.onComparisonPicked)
			self.comparisonPages.append(page)
	
	def createFinalPage(self):
		w = QtGui.QWidget()
		w.setLayout(QtGui.QVBoxLayout())
		w.layout().addWidget(QtGui.QLabel('<center>Completed!<br><br>Please let the researcher know that you are now done.</center>'))
		button = QtGui.QPushButton('Save and close')
		button.clicked.connect(self.saveAndClose)
		w.layout().addWidget(button)
		self.tabs.addTab(w, 'Finished')
	
	def onComparisonPicked(self, choice, options):
		self.gotoNextPage()
		
	def gotoNextPage(self):
		current = self.tabs.currentIndex()
		if current == 0 and self.startTime is None:
			self.startTime = time.time()
			
		if current < self.tabs.count():
			self.tabs.setCurrentIndex(current+1)
			self.previousButton.setDisabled(False)
			if current == self.tabs.count() - 2:
				self.nextButton.setDisabled(True)
				
		self.unfocus()
		
	def gotoPreviousPage(self):
		current = self.tabs.currentIndex()
		if current > -1:
			self.tabs.setCurrentIndex(current-1)
			self.nextButton.setDisabled(False)
			if current == 1:
				self.previousButton.setDisabled(True)
		
		self.unfocus()

	def unfocus(self):
		w = QtGui.QApplication.focusWidget()
		if w is not None:
			w.clearFocus()
			
	def saveAndClose(self):
		rawScores = {}
		weights = {}
		
		for f in factors:
			rawScores[f['name']] = self.sliders[f['name']].value()
			weights[f['name']] = 0
			
		for p in self.comparisonPages:
			weights[p.getChoice()] += 1

		outputFilename = settings.value('Output filename', 'nasa-tlx-output.csv')
		if not os.path.isfile(outputFilename):
			with open(outputFilename, 'w') as outputFile:
				outputFile.write('ParticipantID,Start time,Stop time')
				for f in factors:
					outputFile.write(',%s raw' % f['name'])
				for f in factors:
					outputFile.write(',%s count' % f['name'])
				for f in factors:
					outputFile.write(',%s weighted' % f['name'])
				outputFile.write('\n')
			
		with open(outputFilename, 'a') as outputFile:
			outputFile.write(self.participantID.text())
			outputFile.write(',%d' % self.startTime)
			outputFile.write(',%d' % time.time())
			for f in factors:
				outputFile.write(',%d' % rawScores[f['name']])
			for f in factors:
				outputFile.write(',%d' % weights[f['name']])
			for f in factors:
				outputFile.write(',%d' % (rawScores[f['name']] * weights[f['name']] / 15))
			outputFile.write('\n')
				
		self.close()

if __name__ == '__main__':
	import sys

	app = QtGui.QApplication(sys.argv)
	appWindow = TLXWindow()
	if settings.value('Show fullscreen', True):
		appWindow.showFullScreen()
	else:
		appWindow.showMaximized()
	sys.exit(app.exec_())
