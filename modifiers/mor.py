class metadata:
	name="mor"
	version="1.0.0.0"
	description="Say things backwards"
	type="Modifier"

active=False

def action(bot,io,data):
	return data[::-1]