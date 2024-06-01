import tomlkit

# Load the existing pyproject.toml
with open("pyproject.toml", "r") as file:
    pyproject_data = tomlkit.parse(file.read())

# Add the packages section
pyproject_data["tool"]["poetry"]["packages"] = [{"include": "weather_chatbot"}]

# Save the updated pyproject.toml
with open("pyproject.toml", "w") as file:
    file.write(tomlkit.dumps(pyproject_data))

print("Updated pyproject.toml with packages section.")
