import io
import sys

from pythonCode import jello

if __name__ == '__main__':
    program, *args = sys.argv
    if len(args) == 0:
        print(f"Usage: {program} <path/to/Main.class>")
        print(f"ERROR: no path to Main.class was provided")
        exit(1)
    file_path, *args = args
    clazz = jello.parse_class_file(file_path)
    [main] = jello.find_methods_by_name(clazz, b'main')
    [code] = jello.find_attributes_by_name(clazz, main['attributes'], b'Code')
    code_attrib = jello.parse_code_info(code['info'])
    jello.execute_code(clazz, code_attrib['code'])
  
