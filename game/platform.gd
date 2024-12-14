extends StaticBody2D


# Called when the node enters the scene tree for the first time.
func _ready():
	modulate = Color(Color.MEDIUM_SEA_GREEN, 0.7)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	visible = global.is_dragging
