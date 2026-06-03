extends Node2D

const GRAVITY = 1800.0
const JUMP_VELOCITY = -520.0
const OBSTACLE_SPEED = 320.0
const MIN_SPAWN_INTERVAL = 1.0
const MAX_SPAWN_INTERVAL = 2.2

var player_pos = Vector2(150, 0)
var player_vel = Vector2.ZERO
var player_size = Vector2(40, 50)
var score = 0
var high_score = 0
var game_over = false
var started = false
var obstacle_timer = 0.0
var next_spawn = 1.5
var obstacles = []
var ground_y = 520.0
var player_on_ground = true

@onready var score_label = $ScoreLabel
@onready var game_over_label = $GameOverLabel
@onready var restart_button = $RestartButton
@onready var start_label = $StartLabel

func _ready():
	score_label.text = "Score: 0"
	game_over_label.visible = false
	restart_button.visible = false
	start_label.text = "Tap or Click to Start"
	start_label.visible = true

func reset_game():
	player_pos = Vector2(150, ground_y - player_size.y)
	player_vel = Vector2.ZERO
	score = 0
	game_over = false
	started = true
	obstacle_timer = 0.0
	next_spawn = 1.5
	obstacles.clear()
	for child in get_tree().get_nodes_in_group("obstacles"):
		child.queue_free()
	score_label.text = "Score: 0"
	game_over_label.visible = false
	restart_button.visible = false
	start_label.visible = false

func jump():
	if not started:
		reset_game()
		return
	if game_over:
		return
	if player_on_ground:
		player_vel.y = JUMP_VELOCITY
		player_on_ground = false

func _input(event):
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		jump()
	if event is InputEventScreenTouch and event.pressed:
		jump()
	if event is InputEventKey and event.pressed and event.keycode == KEY_SPACE:
		jump()

func _process(delta):
	if game_over or not started:
		return
	
	player_vel.y += GRAVITY * delta
	player_pos += player_vel * delta
	
	if player_pos.y >= ground_y - player_size.y:
		player_pos.y = ground_y - player_size.y
		player_vel.y = 0
		player_on_ground = true
	
	spawn_obstacles(delta)
	move_obstacles(delta)
	check_collisions()
	update_score(delta)
	queue_redraw()

func spawn_obstacles(delta):
	obstacle_timer += delta
	if obstacle_timer >= next_spawn:
		obstacle_timer = 0
		next_spawn = randf_range(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)
		var obs_h = randf_range(40, 100)
		var obs = {
			"pos": Vector2(1300, ground_y - obs_h),
			"size": Vector2(30, obs_h),
			"scored": false
		}
		obstacles.append(obs)

func move_obstacles(delta):
	var to_remove = []
	for obs in obstacles:
		obs.pos.x -= OBSTACLE_SPEED * delta
		if obs.pos.x < -50:
			to_remove.append(obs)
	for obs in to_remove:
		obstacles.erase(obs)

func check_collisions():
	var player_rect = Rect2(player_pos.x - player_size.x/2, player_pos.y, player_size.x, player_size.y)
	for obs in obstacles:
		var obs_rect = Rect2(obs.pos.x - obs.size.x/2, obs.pos.y, obs.size.x, obs.size.y)
		if player_rect.intersects(obs_rect):
			on_game_over()
			return

func update_score(delta):
	for obs in obstacles:
		if not obs.scored and obs.pos.x + obs.size.x/2 < player_pos.x:
			obs.scored = true
			score += 1
	score_label.text = "Score: %d" % score

func on_game_over():
	game_over = true
	game_over_label.text = "Game Over!\nScore: %d" % score
	game_over_label.visible = true
	restart_button.text = "Restart"
	restart_button.visible = true

func _on_restart():
	reset_game()

func _on_start():
	reset_game()

func _draw():
	draw_rect(Rect2(Vector2(0, 0), Vector2(1280, 720)), Color(0.1, 0.1, 0.1))
	draw_rect(Rect2(Vector2(0, ground_y), Vector2(1280, 720 - ground_y)), Color(0.2, 0.6, 0.2))
	draw_rect(Rect2(player_pos.x - player_size.x/2, player_pos.y, player_size.x, player_size.y), Color(0.7, 0.7, 0.7))
	draw_circle(Vector2(player_pos.x - 8, player_pos.y + 12), 4, Color(0, 0, 0))
	draw_circle(Vector2(player_pos.x + 8, player_pos.y + 12), 4, Color(0, 0, 0))
	for obs in obstacles:
		draw_rect(Rect2(obs.pos.x - obs.size.x/2, obs.pos.y, obs.size.x, obs.size.y), Color(0.8, 0.2, 0.2))
