from Pipeline import *

if __name__ == "__main__":

    pipeline = Pipeline("kosice", 20, debug=False)
    pipeline.data_to_db()