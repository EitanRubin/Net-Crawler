"""Main entry point for API mapping system."""
import asyncio
import json
import argparse
import sys
from pathlib import Path
from config_loader import load_config
from api_mapper import APIMapper


async def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='API Mapping System')
    parser.add_argument('--config', '-c', required=True, help='Path to configuration JSON file')
    parser.add_argument('--output', '-o', help='Output file path (overrides config)')
    
    args = parser.parse_args()

    # Load configuration
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)

    try:
        config = load_config(str(config_path))
        print("Configuration loaded successfully")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

    # Override output file if provided
    if args.output:
        config.output_file = args.output

    # Create mapper
    mapper = APIMapper(config)

    try:
        # Initialize
        await mapper.initialize()
        print("Browser initialized")

        # Run mapping
        result = await mapper.map_website()

        # Save output
        output_path = Path(config.output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Mapping complete!")
        print(f"✓ Found {len(result.get('api_calls', []))} unique api calls")
        print(f"✓ Results saved to: {output_path}")

    except KeyboardInterrupt:
        print("\n\nMapping interrupted by user")
    except Exception as e:
        print(f"\nError during mapping: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await mapper.cleanup()
        print("Cleanup complete")


if __name__ == '__main__':
    asyncio.run(main())

