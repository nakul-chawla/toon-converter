"""CLI tool for TOON converter."""

import argparse
import sys
import json
from pathlib import Path
from toon_converter import json_to_toon, toon_to_json, validate_json, validate_toon


def convert_file(input_path: str, output_path: str = None):
    """Convert file between JSON and TOON formats."""
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Error: File '{input_path}' not found")
        sys.exit(1)
    
    content = input_file.read_text(encoding='utf-8')
    
    # Detect format by extension
    if input_file.suffix.lower() == '.json':
        # JSON to TOON
        try:
            result = json_to_toon(content)
            output_ext = '.toon'
        except Exception as e:
            print(f"Error converting JSON to TOON: {e}")
            sys.exit(1)
    elif input_file.suffix.lower() == '.toon':
        # TOON to JSON
        try:
            data = toon_to_json(content)
            result = json.dumps(data, indent=2)
            output_ext = '.json'
        except Exception as e:
            print(f"Error converting TOON to JSON: {e}")
            sys.exit(1)
    else:
        print(f"Error: Unsupported file extension '{input_file.suffix}'")
        print("Supported extensions: .json, .toon")
        sys.exit(1)
    
    # Determine output path
    if output_path:
        output_file = Path(output_path)
    else:
        output_file = input_file.with_suffix(output_ext)
    
    # Write output
    output_file.write_text(result, encoding='utf-8')
    print(f"✓ Converted '{input_path}' -> '{output_file}'")


def validate_file(input_path: str):
    """Validate JSON or TOON file."""
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Error: File '{input_path}' not found")
        sys.exit(1)
    
    content = input_file.read_text(encoding='utf-8')
    
    if input_file.suffix.lower() == '.json':
        is_valid, error = validate_json(content)
        format_name = "JSON"
    elif input_file.suffix.lower() == '.toon':
        is_valid, error = validate_toon(content)
        format_name = "TOON"
    else:
        print(f"Error: Unsupported file extension '{input_file.suffix}'")
        sys.exit(1)
    
    if is_valid:
        print(f"✓ Valid {format_name}: '{input_path}'")
    else:
        print(f"✗ Invalid {format_name}: '{input_path}'")
        print(f"  {error}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='TOON Converter - Convert between JSON and TOON formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  toon convert input.json -o output.toon
  toon convert input.toon -o output.json
  toon validate input.toon
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert between formats')
    convert_parser.add_argument('input', help='Input file path')
    convert_parser.add_argument('-o', '--output', help='Output file path (optional)')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate file format')
    validate_parser.add_argument('input', help='Input file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'convert':
        convert_file(args.input, args.output)
    elif args.command == 'validate':
        validate_file(args.input)


if __name__ == '__main__':
    main()
