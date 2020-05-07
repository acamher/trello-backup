# trello-backup
Translate trello.json in a HTML file for backup pourpose, via command line
## How to use
1. Export the board on a JSON file
2. Save file as 'trello.json' in the same folder where is Python program downloaded
3. Execute file
4. HTML file will be created in the python program folder
4. Save HTML result in your backup folder

###Usage
trello-json.py [-h] [-d DATE] [-i INPUT] [-o OUTPUT] [--dir DIR] [-m] [-l LIST]

####Arguments
**date** - To process changes until the 'date'. In the form of 'DDMMYYYY' (%d%m%Y)

optional arguments:<br/>
**-h, --help**    Show this help message and exit<br/>
**-d DATE, --date DATE**  To process changes in JSON file until the 'date'<br/>
**-i INPUT, --input INPUT** JSON file input<br/>
**-o OUTPUT, --output OUTPUT** HTML file input<br/>
**--dir DIR**             Directory in batch mode<br/>
**-m, --movedCards**      Check cards moved in the 'date'<br/>
**-l LIST, --list LIST**  List Name to check cards moved<br/>