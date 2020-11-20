####################################################################################
#
# Script for driving a Command Station to execute DCS Conformance Tests
#
# by Erich Whitney
#
####################################################################################
import java
import javax.swing
import jmri

####################################################################################
#
# NMRA DCS Conformance Test Class
#
# This class encapsulates the JMRI actions needed to execute each
# DCS conformance test.
#
####################################################################################	
import collections
import inspect

class DCSConformanceTests:

#-----------------------------------------------------------------------------------
#
# Common Class Functions for setup and test execution
#
#-----------------------------------------------------------------------------------
	def __init__(self):
		self.test = {}	# dictionary of tests
		self.jmri_speed_steps = [ 0.0,	# STOP
								  1.0/28.0,  2.0/28.0,  3.0/28.0,  4.0/28.0,  5.0/28.0,  6.0/28.0,  7.0/28.0,	# speed steps 1-7
								  8.0/28.0,  9.0/28.0, 10.0/28.0, 11.0/28.0, 12.0/28.0, 13.0/28.0, 14.0/28.0, 	# speed steps 8-14
								 15.0/28.0, 16.0/28.0, 17.0/28.0, 18.0/28.0, 19.0/28.0, 20.0/28.0, 21.0/28.0, 	# speed steps 15-21
								 22.0/28.0, 23.0/28.0, 24.0/28.0, 25.0/28.0, 26.0/28.0, 27.0/28.0, 28.0/28.0,	# speed steps 22-28
								 -1.0]	# ESTOP
		self.jmri_speed_step_mode = 28
		self.jmri_throttle_direction = True
		self.jmri_test_throttle_address = 3
		self.jmri_test_throttle_address_long = False
		self.jmri_test_throttle_speed = 0.0
		self.jmri_test_throttle_speed_step = 0
	#--------------------------------------------------------------------------
	#
	# Returns a sorted list of all of the tests registered in this class
	#
	#--------------------------------------------------------------------------
	def getTestList(self):
		items = collections.OrderedDict(sorted(self.test.items()))
		return sorted(items.keys())
	#--------------------------------------------------------------------------
	#
	# Searches the methods defined in this class and builds a list
	# of all methods that implement a test (by naming convention
	#
	#--------------------------------------------------------------------------
	def buildTestList(self):
		mod_list = inspect.getmembers(self)
		for mod in mod_list:
			name = mod[0]
			if name.startswith("test_"):
				listname = name.replace('test_', '')
				listname = listname.replace('dash', '-')
				listname = listname.replace('dot', '.')
				if listname.startswith("S"):
					listname = listname.replace('S', 'Standard S')
				elif listname.startwith("RP"):
					listname = listname.replace('RP', 'Recommended Practice RP')
				print "Adding %s..." % listname
				self.test[listname] = getattr(self, name)
		return
	#--------------------------------------------------------------------------
	#
	# Execute the selected test by name
	#
	# The dcs argument is a handle to the jmri infructure needed
	# to call testing functions such as throttles from the parent class
	#
	#--------------------------------------------------------------------------
	def runTest(self, name, dcs):
		thisTest = self.test[name]
		dcs.status.text = "Test: %s" % name
		thisTest(name, dcs) 
		dcs.status.text = "Test: %s Done." % name
	#--------------------------------------------------------------------------
	#
	# Utility function to wait for a button press and return with an action
	#
	#--------------------------------------------------------------------------
	def waitForProceed(self, dcs):
		while True:
			if dcs.testNext:
				dcs.testNext = False
				return 1
			elif dcs.testPrev:
				dcs.testPrev = False
				return 2
			elif dcs.testDone:
				dcs.testDone = False
				return 0
			elif dcs.testExit:
				dcs.testExit = False
				return -1
#-----------------------------------------------------------------------------------
#
# Common test functions for the JMRI setup features
#
#-----------------------------------------------------------------------------------
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to 128 speed step mode
	#
	#--------------------------------------------------------------------------
	def set128SpeedStepMode(self, dcs):
		dcs.throttle.setSpeedStepMode(jmri.SpeedStepMode.NMRA_DCC_128)
		return
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to 28 speed step mode
	#
	#--------------------------------------------------------------------------
	def set28SpeedStepMode(self, dcs):
		dcs.throttle.setSpeedStepMode(jmri.SpeedStepMode.NMRA_DCC_28)
		return
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to the default speed step mode
	#
	#--------------------------------------------------------------------------
	def setSpeedStepMode(self, dcs):
		if self.jmri_speed_step_mode == 28:
			self.set28SpeedStepMode(dcs)
		elif self.jmri_speed_step_mode == 128:
			self.set128SpeedStepMode(dcs)
		return
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to forward
	#
	#--------------------------------------------------------------------------
	def setThrottleForward(self, dcs):
		dcs.throttle.setIsForward(True)
		return
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to reverse
	#
	#--------------------------------------------------------------------------
	def setThrottleReverse(self, dcs):
		dcs.throttle.setIsForward(False)
		return
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to the default throttle direction
	#
	#--------------------------------------------------------------------------
	def setThrottleDirection(self, dcs):
		dcs.throttle.setIsForward(self.jmri_throttle_direction)
		return
	#--------------------------------------------------------------------------
	#
	# Set the default throttle the given speed step
	#
	#--------------------------------------------------------------------------
	def getThrottleSpeedFromStep(self, step):
		if step < 0 or step > len(self.jmri_speed_steps):
			return 0
		else:
			return self.jmri_speed_steps[step]
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to the given speed value
	#
	#--------------------------------------------------------------------------
	def setThrottleSpeed(self, dcs, speed):
		if (speed == -1 or (speed >= 0 and speed <= 1.0)):
			dcs.throttle.setSpeedSetting(speed)
		return
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to one of the 28 speed steps
	#
	# speeds steps are 0-29
	# 0 = STOP
	# 1-28 are speeds 1-28
	# 29 = ESTOP
	#
	#--------------------------------------------------------------------------
	def setThrottle28SpeedStep(self, dcs, step):
		speed = self.getThrottleSpeedFromStep(step)
		dcs.throttle.setSpeedSetting(speed)
		return
	#--------------------------------------------------------------------------
	#
	# Set the default throttle to one of the 128 speed steps
	#
	# speed steps are 0-127
	# 0 = STOP
	# 1-126 are speeds 1-126
	# 127 = ESTOP
	#
	#--------------------------------------------------------------------------
	def setThrottle128SpeedStep(self, dcs, step):
		if step == 0:
			speed = 0.0
		elif step == 127:
			speed = -1.0
		elif speed >= 1 and speed <= 126:
			speed = (step)/126.0
		else:
			return
			
		dcs.throttle.setSpeedSetting(speed)
		return
	#--------------------------------------------------------------------------
	#
	# Get and configure the throttle
	#
	#--------------------------------------------------------------------------
	def configureThrottle(self, dcs):
		try:
			dcs.throttle = dcs.getThrottle(self.jmri_test_throttle_address, self.jmri_test_throttle_address_long)
		except:
			dcs.status.text = "ERROR: Couldn't assign throttle: %d" % self.jmri_test_throttle_address
			return

		self.setSpeedStepMode(dcs)
		self.setThrottleDirection(dcs)
#-----------------------------------------------------------------------------------
#
# Common Test Templates
#
# 1) Configure necessary buttons
# 2) Configure the throttle (if used)
# 3) Execute the test
#
# The calling method needs to set the global JMRI settings before calling this code
#-----------------------------------------------------------------------------------
	#------------------------------------------------
	#
	# Run through the speeds steps for a given throttle
	# 	
	#------------------------------------------------
	def speed28Steps(self, name, dcs):
		#
		# Configure global test settings
		#
		self.jmri_speed_step_mode = 28
		#
		# Configure the necessary buttons for this test
		#
		dcs.startButton.enabled = False
		dcs.exitButton.enabled = False
		dcs.nextButton.enabled = True
		dcs.prevButton.enabled = True
		dcs.doneButton.enabled = True
		#
		# Configure the throttle
		#
		self.configureThrottle(dcs)
		#
		# Execute the test
		#
		step = 0
		last = len(self.jmri_speed_steps)-1
		done = False
		if self.jmri_throttle_direction:
			thdir = "FWD"
		else:
			thdir = "REV"
		while not done:
			if step == 0:
				dcs.prevButton.enabled = False
			else:
				dcs.prevButton.enabled = True
			if step == last:
				dcs.nextButton.enabled = False
			else:
				dcs.nextButton.enabled = True

			speed = self.getThrottleSpeedFromStep(step)
			dcs.status.text = "Address = %d, %s Step %d, Throttle Value: %7.3f" % (self.jmri_test_throttle_address, thdir, step, speed)
			self.setThrottle28SpeedStep(dcs, step)
			action = self.waitForProceed(dcs)
			if action == 1:
				step = step + 1
			elif action == 2:
				step = step - 1
			elif action == 0:
				done = True

		step = 0
		speed = self.getThrottleSpeedFromStep(step)
		self.setThrottle28SpeedStep(dcs, step)

		dcs.status.text = "Test %s Done." % name
		return
#-----------------------------------------------------------------------------------
#
# Test methods--all must take the same arguments
#
# Test method naming convention:
#
# MUST start with 'test_'
# Then must contain either 'S' or 'RP' for Standard or Recommended Practice
# Use the word 'dash' to insert a '-' in the name
# Use the word 'dot' to inssert a '.' in the name
#
# Example:
# def test_Sdash9dot1dashAdot1(self, name, dcs):
# Will become 'Standard S-9.1-A.1'
#
# Each test shall follow these basic templates:
#
#------------------------------------------------
#
# Case 1: just a few basic steps
#
#------------------------------------------------
#def test_Sdash9dot1dashAdot1dash4(self, name, dcs):
#	#
#	# Configure global test settings
#	#
#	self.jmri_test_throttle_address_long = False
#	self.jmri_test_throttle_address = 3
#	self.jmri_speed_step_mode = 28
#	#
#	# Configure the necessary buttons for this test
#	#
#	dcs.startButton.enabled = False
#	dcs.exitButton.enabled = False
#	#
#	# Configure the throttle
#	#
#	self.configureThrottle(dcs)
#	#
#	# Execute the test
#	#
#	speed = 0.0
#	dcs.status.text = "Address = %d, Speed set to %f" % (self.jmri_test_throttle_address, speed)
#	self.setThrottleSpeed(dcs, speed)
#	return
#------------------------------------------------
# 
# Case 2: using a helper function for common setups
#
#------------------------------------------------
#def test_Sdash9dot2dashAdot1(self, name, dcs):  
#    #                                           
#    # Configure global test settings            
#    #                                           
#    self.jmri_throttle_direction = True         
#    self.jmri_test_throttle_address = 3         
#    self.jmri_test_throttle_address_long = False
#    self.jmri_speed_step_mode = 28              
#    #                                           
#    # Call the common test code                 
#    #                                           
#    self.speed28Steps(name, dcs)                
#------------------------------------------------
	#-----------------------------------------------------------------------------------
	#
	# S-9.1-A.1-4, regular DCC packets, cab at stop
	#	
	#-----------------------------------------------------------------------------------
	def test_Sdash9dot1dashAdot1dash4(self, name, dcs):
		#
		# Configure global test settings
		#
		self.jmri_throttle_direction = True
		self.jmri_test_throttle_address_long = False
		self.jmri_test_throttle_address = 3
		self.jmri_speed_step_mode = 28
		#
		# Configure the necessary buttons for this test
		#
		dcs.startButton.enabled = False
		dcs.exitButton.enabled = False
		#
		# Configure the throttle
		#
		self.configureThrottle(dcs)
		#
		# Execute the test
		#
		if self.jmri_throttle_direction:
			thdir = "FWD"
		else:
			thdir = "REV"
		speed = 0.0
		dcs.status.text = "Address = %d, %s Speed set to %f" % (self.jmri_test_throttle_address, thdir, speed)
		self.setThrottleSpeed(dcs, speed)
		return
	#-----------------------------------------------------------------------------------
	#
	# S-9.1-A.5-6, stritch 0's, cab 0 at full speed
	#	
	#-----------------------------------------------------------------------------------
	def test_Sdash9dot1dashAdot5dash6(self, name, dcs):
		#
		# Configure global test settings
		#
		self.jmri_throttle_direction = True
		self.jmri_test_throttle_address_long = False
		self.jmri_test_throttle_address = 0
		self.jmri_speed_step_mode = 28
		#
		# Configure the necessary buttons for this test
		#
		dcs.startButton.enabled = False
		dcs.exitButton.enabled = False
		dcs.nextButton.enabled = True
		#
		# Configure the throttle
		#
		self.configureThrottle(dcs)
		#
		# Execute the test
		#
		if self.jmri_throttle_direction:
			thdir = "FWD"
		else:
			thdir = "REV"
		step = 28
		speed = self.getThrottleSpeedFromStep(step)
		dcs.status.text = "Address = %d, %s Step %d, Throttle Value: %7.3f" % (self.jmri_test_throttle_address, thdir, step, speed)
		self.setThrottle28SpeedStep(dcs, step)
		action = self.waitForProceed(dcs)
		if action == 1:
			step = 0
			dcs.throttle.setSpeedSetting(speed)
			dcs.status.text = "Test %s Done." % name
		return
	#-----------------------------------------------------------------------------------
	#
	# S-9.2-A.1, 28 speed steps forward
	#	
	#-----------------------------------------------------------------------------------
	def test_Sdash9dot2dashAdot1(self, name, dcs):
		#
		# Configure global test settings
		#
		self.jmri_throttle_direction = True
		self.jmri_test_throttle_address = 3
		self.jmri_test_throttle_address_long = False
		#
		# Call the common test code
		#
		self.speed28Steps(name, dcs)
	#-----------------------------------------------------------------------------------
	#
	# S-9.2-A.2, 28 speed steps reverse
	#	
	#-----------------------------------------------------------------------------------
	def test_Sdash9dot2dashAdot2(self, name, dcs):
		#
		# Configure global test settings
		#
		self.jmri_throttle_direction = False
		self.jmri_test_throttle_address = 3
		self.jmri_test_throttle_address_long = False
		#
		# Call the common test code
		#
		self.speed28Steps(name, dcs)
####################################################################################
#
# Create an instance of the AbstractAutomation class 
#
####################################################################################	

class DCCCommandStationControl(jmri.jmrit.automat.AbstractAutomaton) :
#-----------------------------------------------------------------------------------
#
# self.init() called exactly once at the startup to do any necessary configuration
#
#-----------------------------------------------------------------------------------
	def init(self) :

		self.testExit = False
		
		self.scriptversion = "0.0.1"
		
		print "DCS Control Script Version %s" % self.scriptversion
		self.scriptState = "wait"
		self.testNext = False
		self.testPrev = False
		self.testDone = False
		return
#-----------------------------------------------------------------------------------
#
# self.handle(), called by self.start()
#
# This calls the selected test from the GUI
#
#-----------------------------------------------------------------------------------
	def handle(self):

		self.startButton.enabled = True
		self.exitButton.enabled = True
		self.nextButton.enabled = False
		self.prevButton.enabled = False
		self.doneButton.enabled = False

		while self.scriptState == "wait":
			if self.testExit:
				self.frame.dispose()
				return False
			
		thisTest = self.testID.getSelectedItem()

		self.scriptState = "run"
		
		self.nmraTests.runTest(thisTest, self)

		self.scriptState = "wait"
		return not self.testExit
#-----------------------------------------------------------------------------------
#
# define what buttons do when clicked and attach that routine to the button
#
#-----------------------------------------------------------------------------------
	def whenMyStartButtonClicked(self,event) :
		if self.scriptState == "wait":
			self.scriptState = "run"
			self.startButton.enabled = False
		return

	def whenMyNextButtonClicked(self,event) :
		self.testNext = True
		return

	def whenMyPrevButtonClicked(self,event) :
		self.testPrev = True
		return

	def whenMyDoneButtonClicked(self,event) :
		self.testDone = True
		return

	def whenMyExitButtonClicked(self,event) :
		self.testExit = True
		return
#-----------------------------------------------------------------------------------
#
# This method creates the user input panel, starting the whole process
# the panel collects input parameters from the user
#
#-----------------------------------------------------------------------------------
	def setup(self):
		
		self.nmraTests = DCSConformanceTests()
		self.nmraTests.buildTestList()
		
		# create a frame to hold the button, set up for nice layout
		self.frame = javax.swing.JFrame("DCS Conformance Test Control")		# argument is the frames title
		self.frame.setLocation(400, 600)
		self.frame.setSize(500, 250)
		self.frame.contentPane.setLayout(javax.swing.BoxLayout(self.frame.contentPane, javax.swing.BoxLayout.Y_AXIS))

		# create the start button
		self.startButton = javax.swing.JButton("Run")
		self.startButton.actionPerformed = self.whenMyStartButtonClicked
		self.testStartSelect = javax.swing.JLabel("Press 'Run' to execute the selected test")

		self.nextButton = javax.swing.JButton("Next")
		self.nextButton.actionPerformed = self.whenMyNextButtonClicked
		self.testNextSelect = javax.swing.JLabel("Press 'Next' for next step")

		self.prevButton = javax.swing.JButton("Prev")
		self.prevButton.actionPerformed = self.whenMyPrevButtonClicked
		self.testPrevSelect = javax.swing.JLabel("Press 'Prev' for previous")

		self.doneButton = javax.swing.JButton("Done")
		self.doneButton.actionPerformed = self.whenMyDoneButtonClicked
		self.testDoneSelect = javax.swing.JLabel("Press 'Done' when done with test")

		self.exitButton = javax.swing.JButton("Exit")
		self.exitButton.actionPerformed = self.whenMyExitButtonClicked
		self.testExitSelect = javax.swing.JLabel("Press 'Exit' when done")


		self.testIDLabel = javax.swing.JLabel("", javax.swing.JLabel.CENTER)
		self.testIDLabel.setText("Select Test")

		self.status = javax.swing.JLabel("Test Status", javax.swing.JLabel.CENTER)
		
		self.testID = javax.swing.JComboBox()
		for test in self.nmraTests.getTestList():
			self.testID.addItem(test)

		self.panel = javax.swing.JPanel()
		self.frame.contentPane.add(self.testIDLabel)
		self.frame.contentPane.add(self.testID)
		self.panel.add(self.startButton)
		self.panel.add(self.nextButton)
		self.panel.add(self.prevButton)
		self.panel.add(self.doneButton)
		self.panel.add(self.exitButton)
		self.frame.contentPane.add(self.panel)
		self.frame.contentPane.add(self.testStartSelect)
		self.frame.contentPane.add(self.testNextSelect)
		self.frame.contentPane.add(self.testPrevSelect)
		self.frame.contentPane.add(self.testDoneSelect)
		self.frame.contentPane.add(self.testExitSelect)
		self.frame.contentPane.add(self.status)
		self.frame.pack()
		self.frame.show()
		self.frame.setLocation(400, 600)
		self.frame.setSize(500, 250)
		self.start()
		return
#-----------------------------------------------------------------------------------
#
# Instantiate the automation class and start it up
#
#-----------------------------------------------------------------------------------
a = DCCCommandStationControl()

# set the name, as a example of configuring it
a.setName("DCS Conformance Test Control")

# This brings up the dialog box that will call self.start()
a.setup()
