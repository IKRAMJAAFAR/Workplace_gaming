extends Node2D

# Load the item scene
const ITEM_SCENE = preload("res://scene/items.tscn")  # Replace with the correct path

@onready var spawn_timer = $SpawnTimer

func _ready():
	if spawn_timer:  # Ensure the timer exists
		spawn_timer.wait_time = 2.0  # Time interval for spawning
		spawn_timer.start()  # Start the timer
		spawn_timer.timeout.connect(_on_spawn_timer_timeout)
	else:
		print("Error: SpawnTimer node not found!")

# Function to spawn items at random positions
func _on_spawn_timer_timeout():
	if not ITEM_SCENE:    
		print("Error: ITEM_SCENE is null!")
		return
	
	var item_instance = ITEM_SCENE.instance()  # Create an instance of the item
	add_child(item_instance)  # Add item to the scene
	
	# Randomize position (adjust to fit your game area)
	item_instance.position = Vector2(randf() * 800, 0)  # Random X, Y starts at 0
	if randi() % 2 == 0:
		item_instance.item_type =  "Recycle"
	else:
		item_instance.item_type = "Trash"  # Random type
