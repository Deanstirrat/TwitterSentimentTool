# TwitterSentimentTool

This tool takes in search groups and locations to find current twitter user sentiment for the given topic. Results are displayed in the form of a easy to read pie chart

## Usage
Before running, add your input values as follows:

numTimesToRun - number of times to run the entire program through, this is an unbounded integer.

numOfTweets - number of tweets to retieve for each search group. This is an unbounded number, but keep in mind, if the location you are searching in is sparsley populated, or has a low number of twitter users, the stream API may take a long time to find the desired number of tweets.

searchParams - 2 python dictionaries. The first holding locations with their name mapped to bottom left and top right latitudinal/longitudinal coordinates forming a box around the desired location to search in. The second being a dictionary of searhc group names to a comma seperated list of search terms to look for.
```python
#EXAMPLE INPUT
numTimesToRun = 1
numOfTweets = 50
searchParams = {
    "locations" : {
        "Helsinki Finland" : '24.840226, 60.146301, 25.068389, 60.243535',
        "Bengaluru" : '77.522668,12.925527,77.691964,13.035670',
        "United States" : '-122.986677,25.847657,-58.636563,44.852504'
    },
    "searchGroups" : {
        "pro-russian" : 'Russia,Putin',
        "pro-ukrainin" : 'Ukraine,nato,zelensky'
    }
}
```