const fs = require('fs');
const path = require('path');

class Parser {
    constructor(filePath) {
        this.filePath = path.resolve(filePath);
    }

    parse() {
        if (!fs.existsSync(this.filePath)) {
            throw new Error(`File not found: ${this.filePath}`);
        }

        const fileContent = fs.readFileSync(this.filePath, 'utf-8');
        return this._processContent(fileContent);
    }

    _processContent(content) {
        const lines = content.split('\n');
        return lines.map(line => line.trim()).filter(line => line.length > 0);
    }

    static validateFileExtension(filePath, validExtensions) {
        const ext = path.extname(filePath).toLowerCase();
        return validExtensions.includes(ext);
    }
}

module.exports = Parser;