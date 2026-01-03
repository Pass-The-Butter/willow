from dotenv import load_dotenv
import os

with open('.env.test', 'w') as f:
    f.write('TEST_VAR=foo$$bar\n')

load_dotenv('.env.test')
val = os.getenv('TEST_VAR')
print(f"Value: '{val}'")
if val == 'foo$bar':
    print("Resolves to single $")
elif val == 'foo$$bar':
    print("Resolves to double $$")
