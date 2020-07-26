const fs = require('fs');
const readline = require('readline');
const { google } = require('googleapis');

// If modifying these scopes, delete token.json.
const SCOPES = [
  'https://www.googleapis.com/auth/documents',
  'https://www.googleapis.com/auth/drive',
];
// The file token.json stores the user's access and refresh tokens, and is
// created automatically when the authorization flow completes for the first
// time.
const TOKEN_PATH = 'token.json';

/**
 * Get and store new token after prompting for user authorization, and then
 * execute the given callback with the authorized OAuth2 client.
 * @param {google.auth.OAuth2} oAuth2Client The OAuth2 client to get token for.
 */
function getAccessToken(oAuth2Client, callback, ...args) {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });
  console.log('Authorize this app by visiting this url:', authUrl);
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question('Enter the code from that page here: ', (code) => {
    rl.close();
    oAuth2Client.getToken(code, (err, token) => {
      if (err) return console.error('Error retrieving access token', err);
      oAuth2Client.setCredentials(token);
      // Store the token to disk for later program executions
      fs.writeFile(TOKEN_PATH, JSON.stringify(token), (errWrite) => {
        if (errWrite) return console.error(errWrite);
        return console.log('Token stored to', TOKEN_PATH);
      });
      return callback(oAuth2Client, args);
    });
  });
}

/**
 * Create an OAuth2 client with the given credentials, and then execute the
 * given callback function.
 * @param {Object} credentials The authorization client credentials.
 * @param {function} callback The callback to call with the authorized client.
 */
function authorize(credentials, callback, ...args) {
  const { clientSecret, clientID, redirectUris } = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(
    clientID, clientSecret, redirectUris[0],
  );

  // Check if we have previously stored a token.
  fs.readFile(TOKEN_PATH, (err, token) => {
    if (err) return getAccessToken(oAuth2Client, callback, ...args);
    oAuth2Client.setCredentials(JSON.parse(token));
    return callback(oAuth2Client, args);
  });
}

function callWithCredentials(callback, ...args) {
  // Load client secrets from a local file.
  fs.readFile('credentials.json', (err, content) => {
    if (err) return console.log('Error loading client secret file:', err);
    // Authorize a client with credentials, then call the Google Drive API.
    return authorize(JSON.parse(content), callback, args);
  });
}

/**
 * Get Google Drive folder ID by its name.
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 * @param {string} folderName Folder name.
 */
function getFolderID(auth, folderName) {
  const drive = google.drive({ version: 'v3', auth });
  drive.files.list({
    q: `mimeType='application/vnd.google-apps.folder' 
        and name='${folderName}' and not trashed`,
    fields: 'files(id)',
  }, (err, res) => {
    if (err) return console.log(`The API returned an error: ${err}`);
    const folders = res.data.files;
    if (!folders.length) return console.log(`${folderName} is not found in Google Drive.`);
    return folders[0].id;
  });
}

/**
 * Lists the names and IDs of Google Docs for provided folder.
 * @param {google.auth.OAuth2} auth An authorized OAuth2 client.
 * @param {string} folderID Id of a folder.
 */
function listDocs(auth, folderID) {
  const drive = google.drive({ version: 'v3', auth });
  drive.files.list({
    q: `mimeType = 'application/vnd.google-apps.document' 
        and '${folderID}' in parents and not trashed`,
    fields: 'files(id, name)',
  }, (err, res) => {
    if (err) return console.log(`The API returned an error: ${err}`);
    return res.data.files;
  });
}

export default {
  callWithCredentials,
  getAccessToken,
  getFolderID,
  listDocs,
};
