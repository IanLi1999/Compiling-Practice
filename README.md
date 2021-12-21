# Syntax Analyzer Exercise Report    

## Result    

Implement a basic syntax analyzer with Python, features including: 

1. Generate **FIRST SET** and **FOLLOW SET** of non-terminal symbols    
  <img src="screenshots/first-follow-set.png" style="zoom:40%;" />

2. Generate **Canonical Collection** of LR(0) items    
  <img src="screenshots/canonical-collection.png" style="zoom:50%;" />   

3. Generate **SLR Analyzing Table**  
  <img src="screenshots/analyzing-table.png" style="zoom: 33%;" />  
  
  >  `-1` represents `ERROR` status  

4. Generate analyze proecss    
  <img src="screenshots/analyze.png" style="zoom: 33%;" /> 

Run `python3 Syntax.py` to see the above results. Only the 4th step is shown in the console, other steps' outputs are stored in the `Syntax Result.txt`.   

## Project Structure    

### Text Files    

`Syntax Result.txt` stores the output.  

`Syntatic Analyzer Test File.txt` is the test file for syntax analyzer.   

### Automation.py  

`Automation.py`
Methods to be used in the analyze progress.  
- `cal_first(), cal_follow(), cal_first_follow()` 　
- `generate_collections(), partition(), calculate_closure()`  
- `generate_table(), fill_table()`  


### Syntax.py  

The analyze process, calling methods in Automation.  

- `analyze()`  
- `process(), make_action()`  
