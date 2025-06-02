# MyFS Project

MyFS is a secure file management system designed to create, manage, and protect files within a virtual volume. The system allows users to import and export files while ensuring data security, integrity, and recovery options.

## Features

- **Volume Creation**: Create and format a MyFS volume (MyFS.DRI) with metadata.
- **Password Management**: Set, change, and verify passwords for accessing the MyFS volume and individual files.
- **File Management**: Import files into MyFS, export them back to their original locations, and list all files within the volume.
- **Data Security**: Encrypt file contents with unique passwords, ensuring that sensitive information remains protected.
- **Data Integrity**: Check the integrity of files and implement recovery processes for deleted files.
- **System Verification**: Ensure that the application runs on the correct machine that created the MyFS volume.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd myfs-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Follow the on-screen prompts to interact with the MyFS system.

## Testing

To run the tests, use:
```
pytest tests/
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.