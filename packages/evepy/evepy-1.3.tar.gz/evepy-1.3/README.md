# EVE
A lightweight data-interchange format.

\s\s

# Example use
example.eve
```
[
  @ This is a comment

  @ String variables
  'Name' :: 'Eric'
  'Age' :: '21'
  'Country' :: 'USA'
  'City' :: 'New York'

  @ Boolean variables
  ?hasGirlfriend = False
];
```

example.py
```python
import evepy as eve # Imports evepy, but sets it as eve, so you can type eve instead of evepy

result = eve.load('example.eve') # Sets result to the load function and gives a path
print(result['Name']) # Print variables
result['Age'] = '22' # Sets the age variable to 22 instead of 21
eve.save(result, 'example.eve') # Saves the changed file to the file path
```

\s\s

# ATOM grammar syntax highlighting
1. Copy the folder: `eve` in the `editors\atom` folder
2. Paste that to the `.atom` folder in `C:\Users\yourusername\.atom\packages`
3. Now restart ATOM and it should work
