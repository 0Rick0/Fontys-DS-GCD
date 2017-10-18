# Missing Data

When you get a dataset, some data can be missing. This can be caused by multiple reasons, but can generally be put in a couple of categories.

- Missing Completely At Random 
  - There is no real reason for the data to be missing and does not have anything to do with other data.
- Missing at Random
  - The data that is missing can but it has an underlying reason to be missing. In Europe most people want to disclose their salary information. This doesn't mean they don't earn anything but that they don't want to disclose it. That has to be accounted for. It could for example also be correlated to their salary class.
- Not Missing at Random 
  - There is a clear reason for the data to be missing. This could be that the data was not available at the time, it doesn't apply to the individual, or a specific group doesn't want to fill in a survey.
 
# Violations
Violations are when data does not have the form you excect it to be in.
This can be that the data should be in a specific format, e.g. thousands of euros, an specific set of values (gender for example) or something else.
A missing value can also be a violation, if the datapoint is required.

What you do with these violations can differ. In some cases you can remove the violating record, but the missing value must be MCAR because there may be no correlation.

If this is not the case you need to try to fill in the value or fix it. You could for example search for similar records in the dataset and copy from there, or enter an average value.
There are more methods to fix the value but the technique differs from case to case bases.
   

# Applying
We applied this to a dataset in class we generated our self. I was assigned with the gender column.

One of the problem with the dataset is that it is not filled out seriously. A lot of data is gibberish.

To fix this a couple of techniques come to mind:
## Fix the input form
The input form can be fixed in a couple of ways. Firstly you could limit the number of options: male or female.

There is a slight problem with that technique in the modern day, as not everyone identifies themselves as male or female.
You need to at leas add "other" to accompany everyone.

The other option is to change the field type from  gender to sex. sex does have two values, male or female. 

## Classify existing data
You can try to classify the existing data. As said the problem with the dataset is that very few values are correct.

You can classify for example with the following regexes:
`(?i)(man|male|m|)` or `(?i)(vrouw|female|v|f)`. But this leaves a lot of values empty.

Another option is to dynamically add new valid values, when it does not match any known value.
This would be very practical in normal datasets, but not in this case.

Considering the dataset, Classifying with a regex would be the best option in this case.
The dataset is to dirty to add values dynamically and missing values are not core to this column in this survey.

The missing values that occur after this classification must be considered MCAR.
This is because there is no correlation between the gibberish input and the rest of the data, they entered it for fun.

In a normal case, the missing values should be considered MAR.
The person might not be comfortable with their gender, or they don't fit into the two values.
Dynamic classification would also be a better option in this case.