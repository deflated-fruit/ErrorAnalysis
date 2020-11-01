# ErrorAnalysis
Takes in a mathematical expression as a string and variables with values and errors and outputs the error in the result

TO USE:

Pass in to the funcion `get_error()` the following:
`expr`: This is a mathematical expression as a string. You MUST be explicit with multiplication symbols. Functions (like sin or ln) are not currently supported, nor is raising something to a variable)
`errors`: Pass the value and error for each variable in the expression

eg.

    x_error = 0.005
    y_error = 0.01

    x_value = 24.3
    y_value = 102.234

    result = get_errors("(x^2 + y^2) / (2*y)", x=(x_value, x_error), y=(y_value, y_error))
