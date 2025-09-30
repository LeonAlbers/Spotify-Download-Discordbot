import tools.driveUploader as driveUploader

folder_id = driveUploader.create_folder("SpotifyDownloads")

print(f"Created main folder with ID: {folder_id}")
print("You have to set the PARENT_FOLDER_ID in your .env file to this ID for the bot to work correctly.")