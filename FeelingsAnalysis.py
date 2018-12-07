#Module dependencies
import csv

def getFileColumns(csvReader):
  columns = next(csvReader);
  columns[0] = 'ID';
  return columns;

def getColumnsDictionary(columns):
  index = 0;
  columnsDictionary = {};
  for column in columns:
    columnsDictionary[column] = index;
    index += 1;
  return columnsDictionary;

def cleanRows(rows):
	cleanedRows = [];
	for row in rows:
		cleanedRow = [];
		for element in row:
			newElement = element.replace("\n", ".").replace('"',".").replace('/',".").replace(',',".").replace("'",".").replace('-',".");
			cleanedRow.append(newElement);
		cleanedRows.append(cleanedRow);
	return cleanedRows;

def parseFile(filename):
  csvFile = open(filename, 'r');
  csvReader = csv.reader(csvFile, delimiter = ',');
  columns = getFileColumns(csvReader);
  columnsDictionary = getColumnsDictionary(columns);
  rows = [];
  for row in csvReader:
    rows.append(row);
  return columns, columnsDictionary, cleanRows(rows);

def filterRowsByColumn(rows, columnsDictionary, columns):
  indexes = ([ columnsDictionary[column] for column in columns ]);
  for column in columns:
    newRows = [];
    for row in rows:
      if (row[columnsDictionary[column]]):
        newRows.append(row);
    rows = newRows;
  filteredRows = [];
  for row in rows:
    filteredRow = [ row[index] for index in indexes ];
    filteredRows.append(filteredRow);
  return filteredRows;

def getTypesFrequenciesByColumn(rows, columnsDictionary, column):
  typesFrequencies = {};
  for row in rows:
    element = row[columnsDictionary[column]];
    if (element not in typesFrequencies):
      typesFrequencies[element] = 0;
    typesFrequencies[element] += 1;
  return typesFrequencies;

def analyzeFeelingComment(row, columnsDictionary):
  rating = int(row[columnsDictionary["Rating"]]);
  recommended = int(row[columnsDictionary["Recommended IND"]]);
  positiveFeedbackCount = int(row[columnsDictionary["Positive Feedback Count"]]);
  reviewText = ["'" + row[columnsDictionary["Review Text"]] + "'"];
  if (rating == 3):
    return reviewText + ["NEUTRA"];
  if (rating >= 4):
    return reviewText + ["POSITIVA"];
  if (rating <= 2):
    return reviewText + ["NEGATIVA"];

def createFile(filename, rows, columns):
  with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile);
    writer.writerow(columns);
    for row in rows:
    	writer.writerow(row);


def classifier1(columns, columnsDictionary, rows):
  feelingsColumns = ["Recommended IND", "Rating", "Positive Feedback Count", "Review Text"];
  columnsToFilterDictionary = getColumnsDictionary(feelingsColumns);
  filteredRows = filterRowsByColumn(rows, columnsDictionary, feelingsColumns);
  analyzedRows = [];
  for row in filteredRows:
    analyzedRows.append(analyzeFeelingComment(row, columnsToFilterDictionary));
  createFile('reviewsClasificador01.csv', analyzedRows, ["Review Text", "Sentimiento"]);


def classifier2(columns, columnsDictionary, rows):
  classNameColumns = ["Review Text", "Class Name"];
  columnsToFilterDictionary = getColumnsDictionary(classNameColumns);
  filteredRows = filterRowsByColumn(rows, columnsDictionary, classNameColumns);
  typesFrequenciesByColumn = getTypesFrequenciesByColumn(filteredRows, columnsToFilterDictionary, classNameColumns[1])
  typesToFilter = [x for x in typesFrequenciesByColumn if typesFrequenciesByColumn[x] < 10]
  analyzedRows = [];
  for row in filteredRows:
    if (row[1] not in typesToFilter):
      analyzedRows.append(row);
  createFile('reviewsClasificador02.csv', analyzedRows, ["Review Text", "Class Name"]);


columns, columnsDictionary, rows = parseFile('reviews.csv');
feelingsColumns = ["Recommended IND", "Rating", "Positive Feedback Count", "Review Text"];
columnsToFilterDictionary = getColumnsDictionary(feelingsColumns);
filteredRows = filterRowsByColumn(rows, columnsDictionary, feelingsColumns);
print(columnsToFilterDictionary)
print(columnsDictionary)
classifier1(columns, columnsDictionary, rows);
classifier2(columns, columnsDictionary, rows);