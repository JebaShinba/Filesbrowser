const fs = require('fs');
const path = require('path');
const { MongoClient } = require('mongodb');

let testCases;
try {
    const data = fs.readFileSync(path.join(__dirname || '.', 'test_cases.json'), 'utf-8');
    testCases = JSON.parse(data);
} catch (err) {
    console.error('Error reading or parsing test_cases.json:', err);
    throw err;
}

async function run() {
    const uri = 'mongodb://localhost:27017';
    const client = new MongoClient(uri);

    try {
        await client.connect();
        const database = client.db('your_database_name');
        const filesCollection = database.collection('files');

        // Group files by folder name
        const folderMap = testCases.folders.reduce((acc, folder) => {
            if (!acc[folder.folder_name]) {
                acc[folder.folder_name] = [];
            }
            acc[folder.folder_name].push(...folder.files); // Add files to the folder
            return acc;
        }, {});

        // Iterate over unique folders
        for (const folderName of Object.keys(folderMap)) {
            console.log(`Processing folder: ${folderName}`);

            const files = folderMap[folderName];
            for (const file of files) {
                const fileName = file.file_name;

                const existingFile = await filesCollection.findOne({ file_name: fileName, folder_name: folderName });

                if (!existingFile) {
                    const newFile = {
                        file_name: fileName,
                        folder_name: folderName,
                        is_valid: true,
                        expected_error: 'success',
                        createdAt: new Date(),
                        uploadedBy: 'admin@example.com',
                        baseurl: 'https://demo.filebrowser.org/login',
                        user_name: 'demo',
                        password: 'demo',
                        folder_name1: 'store'
                    };

                    await filesCollection.insertOne(newFile);
                    console.log(`Inserted file: ${fileName} from folder: ${folderName}`);
                }
            }
        }
    } catch (err) {
        console.error('Error inserting files:', err);
    } finally {
        await client.close();
    }
}

run().catch(console.error);
