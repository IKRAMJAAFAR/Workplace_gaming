extends Node2D

# Variables
var time_left = 10 # Set timer to 60 seconds

# References to nodes
@onready var timer_label = $TimeLabel # Label to display the timer
@onready var timer_node = $Timer   # Timer node
# Reference to the score label
@onready var score_label = $ScoreLabel # Label to display score

func _ready():
	# Initialize the timer
	timer_node.wait_time = 1.0  # Timer ticks every 1 second
	timer_node.autostart = true # Automatically start the timer
	timer_node.one_shot = false # Timer will keep looping
	
	# Connect the timeout signal of the Timer node
	timer_node.timeout.connect(_on_timer_timeout)

	# Display initial time
	update_timer_label()
	update_score_label()

# Function to handle timer timeout
func _on_timer_timeout():
	if time_left > 0:
		time_left -= 1 # Decrease time by 1 second
		update_timer_label()
	else:
		timer_node.stop() # Stop the timer when it reaches 0
		print("Time's up!") # Or trigger game over

# Update the timer label display
func update_timer_label():
	timer_label.text = "Time Left: %d" % time_left
	
# Variables
var score = 0 # Initial score

# Function to increase score
func add_score(points: int):
	score += points
	update_score_label()

# Update the score label display
func update_score_label():
	score_label.text = "Score: %d" % score
