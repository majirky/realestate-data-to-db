from Pipeline import *

if __name__ == "__main__":

    pipeline = Pipeline("kosice", 2, debug=True)
    pipeline.data_to_db()