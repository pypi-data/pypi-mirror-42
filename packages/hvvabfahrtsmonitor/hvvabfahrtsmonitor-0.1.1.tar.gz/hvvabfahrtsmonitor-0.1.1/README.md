# HVV Abfahrtsmonitor

To be used with links generated at https://abfahrten.hvv.de/

Generated urls need to be changed to include api/monitors (See Sample file contents)

## Usage

```python
from hvvabfahrtsmonitor import HvvAbfahrtsmonitor
monitor = HvvAbfahrtsmonitor(file, schema_file)
monitor.get_times() #Get a dict of lists of times, in minutes, for when the buses/metros/trains are due next.
```
### Sample file contents (JSON)

```json
{
	"data": [{
			"name": "S",
			"url": "https://abfahrten.hvv.de/api/monitors/a038583f-f72b-4e4e-ba22-9d9903ced316"
		},
		{
			"name": "B",
			"url": "https://abfahrten.hvv.de/api/monitors/f76a6c23-a682-4297-aa99-f815157e2bca"
		}
	]
}
```

### Sample schema_file (JSON schema)

```json
{
  "$schema":"http://json-schema.org/draft-07/schema#",
  "title":"Hvv Schema",
  "definitions":{
    "departure":{
      "type": "object",
      "properties":{
        "delay":{
          "type":"string"
        },
        "direction":{
          "type":"string"
        },
        "hasDelay":{
          "type":"boolean"
        },
        "icon":{
          "type":"object"
        },
        "line":{
          "type":"string"
        },
        "station":{
          "type":"string"
        },
        "time":{
          "type":"string"
        }
      },
      "required": ["hasDelay", "line", "time"]
    }
  },
  "type":"object",
  "properties":{
    "data":{
      "type":"object",
      "properties":{
        "attributes":{
          "type":"object",
          "properties":{
            "departures":{
              "type":"array",
              "items":{"$ref":"#/definitions/departure"}
            }
          }
        }
      }
    }
  }
}
```
