# If you are using fish as your shell, you can use
# this function to create a system-wide alias for hurry
# @source https://fishshell.com/docs/current/index.html#defining-aliases
function hurry
	command python3 ~/Projects/hurry-cli/hurry $argv
end
