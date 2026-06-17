import sys
import pydot
from prov.model import ProvDocument
from prov.dot import prov_to_dot

def main():
    # 1. Check if the file name was provided
    if len(sys.argv) < 2:
        print("Error: Missing PROV-N file name.")
        print("Usage: python generate_graph.py <filename.provn>")
        sys.exit(1)

    # 2. Get the filename from the first command line argument
    input_file = sys.argv[1]
    output_file = input_file.replace('.provn', '.png')
    
    # Handle cases where the input file doesn't end in .provn
    if output_file == input_file:
        output_file += '.png'

    try:
        # 3. Load and convert the PROV-N document
        print(f"Reading {input_file}...")
        document = ProvDocument.deserialize(source=input_file, format='provn')
        
        print("Generating graph layout...")
        dot_graph = prov_to_dot(document)
        
        # 4. Save the output image
        dot_graph.write_png(output_file)
        print(f"Success! Graph saved as: {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' could not be found.")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

if __name__ == "__main__":
    main()
