"""
E2B Sandbox Tools and Utilities
Provides helpful tools for working with KimiK2 in the sandbox environment.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import get_logger

logger = get_logger()


class SandboxTools:
    """Collection of utility tools for the E2B sandbox."""

    def __init__(self, base_dir: str = "/home/user/kimik2"):
        """Initialize sandbox tools."""
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "output"
        self.media_dir = self.base_dir / "media"

    def list_outputs(self, output_type: Optional[str] = None) -> List[Path]:
        """
        List all outputs in the output directory.

        Args:
            output_type: Filter by type ('json', 'txt', 'video', 'all')

        Returns:
            List of output file paths
        """
        outputs = []

        if output_type == "json" or output_type is None:
            outputs.extend(self.output_dir.glob("*.json"))

        if output_type == "txt" or output_type is None:
            outputs.extend(self.output_dir.glob("*.txt"))

        if output_type == "video" or output_type is None:
            outputs.extend(self.media_dir.glob("**/*.mp4"))

        return sorted(outputs, key=lambda p: p.stat().st_mtime, reverse=True)

    def get_latest_output(self, output_type: str = "json") -> Optional[Path]:
        """Get the most recent output file."""
        outputs = self.list_outputs(output_type)
        return outputs[0] if outputs else None

    def read_json_output(self, file_path: Path) -> Dict:
        """Read and parse a JSON output file."""
        with open(file_path, "r") as f:
            return json.load(f)

    def read_narrative(self, file_path: Path) -> str:
        """Read a narrative text file."""
        with open(file_path, "r") as f:
            return f.read()

    def export_output(
        self,
        output_file: Path,
        destination: Path,
        compress: bool = False
    ):
        """
        Export an output file to a destination.

        Args:
            output_file: Source file to export
            destination: Destination path
            compress: Whether to compress the file
        """
        logger.info(f"Exporting: {output_file.name}")

        if compress:
            # Create tar.gz archive
            import tarfile
            archive_name = destination / f"{output_file.stem}.tar.gz"

            with tarfile.open(archive_name, "w:gz") as tar:
                tar.add(output_file, arcname=output_file.name)

            logger.info(f"Exported to: {archive_name}")
        else:
            shutil.copy(output_file, destination)
            logger.info(f"Exported to: {destination / output_file.name}")

    def package_exploration(
        self,
        concept: str,
        include_videos: bool = True
    ) -> Path:
        """
        Package all outputs related to a concept exploration.

        Args:
            concept: Concept name
            include_videos: Whether to include rendered videos

        Returns:
            Path to the packaged archive
        """
        import tarfile

        concept_slug = concept.replace(" ", "_").lower()
        logger.info(f"Packaging exploration: {concept}")

        # Find all related files
        json_files = list(self.output_dir.glob(f"{concept_slug}*.json"))
        txt_files = list(self.output_dir.glob(f"{concept_slug}*.txt"))

        files_to_package = json_files + txt_files

        if include_videos:
            video_files = list(self.media_dir.glob("**/*.mp4"))
            files_to_package.extend(video_files)

        # Create archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = self.output_dir / f"{concept_slug}_package_{timestamp}.tar.gz"

        with tarfile.open(archive_name, "w:gz") as tar:
            for file_path in files_to_package:
                tar.add(file_path, arcname=file_path.name)

        logger.info(f"Package created: {archive_name}")
        logger.info(f"   Files included: {len(files_to_package)}")

        return archive_name

    def cleanup_old_outputs(self, keep_recent: int = 10):
        """
        Clean up old output files, keeping only the most recent ones.

        Args:
            keep_recent: Number of recent files to keep
        """
        logger.info(f"Cleaning up old outputs (keeping {keep_recent} most recent)")

        for ext in ["*.json", "*.txt"]:
            files = sorted(
                self.output_dir.glob(ext),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            # Remove old files
            for old_file in files[keep_recent:]:
                logger.info(f"  Removing: {old_file.name}")
                old_file.unlink()

        logger.info("Cleanup complete")

    def get_storage_usage(self) -> Dict[str, Any]:
        """Get storage usage statistics for the sandbox."""
        def get_dir_size(path: Path) -> int:
            total = 0
            for item in path.rglob("*"):
                if item.is_file():
                    total += item.stat().st_size
            return total

        output_size = get_dir_size(self.output_dir)
        media_size = get_dir_size(self.media_dir)
        total_size = output_size + media_size

        return {
            "output_dir_mb": output_size / (1024 * 1024),
            "media_dir_mb": media_size / (1024 * 1024),
            "total_mb": total_size / (1024 * 1024),
            "output_files": len(list(self.output_dir.glob("*"))),
            "media_files": len(list(self.media_dir.glob("**/*"))),
        }

    def create_exploration_report(self) -> str:
        """Generate a summary report of all explorations."""
        logger.info("Generating exploration report")

        json_files = list(self.output_dir.glob("*.json"))

        report_lines = [
            "=" * 60,
            "KIMIK2 EXPLORATION REPORT",
            "=" * 60,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total explorations: {len(json_files)}",
            "",
            "EXPLORATIONS:",
            ""
        ]

        for json_file in sorted(json_files, key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                data = self.read_json_output(json_file)

                concept = data.get("concept", "Unknown")
                timestamp = data.get("timestamp", "Unknown")
                enriched = "Yes" if data.get("enriched", False) else "No"

                report_lines.extend([
                    f"  Concept: {concept}",
                    f"  Time: {timestamp}",
                    f"  Enriched: {enriched}",
                    f"  File: {json_file.name}",
                    ""
                ])

            except Exception as e:
                logger.warning(f"Skipping {json_file.name}: {e}")

        # Add storage info
        storage = self.get_storage_usage()
        report_lines.extend([
            "",
            "STORAGE USAGE:",
            f"  Output: {storage['output_dir_mb']:.2f} MB ({storage['output_files']} files)",
            f"  Media: {storage['media_dir_mb']:.2f} MB ({storage['media_files']} files)",
            f"  Total: {storage['total_mb']:.2f} MB",
            ""
        ])

        report = "\n".join(report_lines)

        # Save report
        report_file = self.output_dir / f"exploration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, "w") as f:
            f.write(report)

        logger.info(f"Report saved: {report_file}")

        return report

    def convert_video_to_gif(
        self,
        video_file: Path,
        output_file: Optional[Path] = None,
        fps: int = 10,
        width: int = 640
    ) -> Path:
        """
        Convert a video file to GIF.

        Args:
            video_file: Input video file
            output_file: Output GIF file (optional)
            fps: Frames per second for the GIF
            width: Width of the output GIF

        Returns:
            Path to the created GIF
        """
        if output_file is None:
            output_file = video_file.with_suffix(".gif")

        logger.info(f"Converting to GIF: {video_file.name}")

        cmd = [
            "ffmpeg",
            "-i", str(video_file),
            "-vf", f"fps={fps},scale={width}:-1:flags=lanczos",
            "-y",  # Overwrite output file
            str(output_file)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"GIF created: {output_file}")
            return output_file

        except subprocess.CalledProcessError as e:
            logger.error(f"GIF conversion failed: {e.stderr}")
            raise

    def interactive_menu(self):
        """Display an interactive menu for sandbox tools."""
        while True:
            print("\n" + "="*60)
            print("KIMIK2 SANDBOX TOOLS")
            print("="*60)
            print("1. List outputs")
            print("2. View latest output")
            print("3. Create exploration report")
            print("4. Check storage usage")
            print("5. Package exploration")
            print("6. Cleanup old outputs")
            print("7. Exit")
            print("="*60)

            choice = input("\nSelect option (1-7): ").strip()

            if choice == "1":
                outputs = self.list_outputs()
                print(f"\nFound {len(outputs)} outputs:")
                for output in outputs[:20]:  # Show first 20
                    print(f"  - {output.name}")

            elif choice == "2":
                latest = self.get_latest_output()
                if latest:
                    print(f"\nLatest output: {latest.name}")
                    if latest.suffix == ".json":
                        data = self.read_json_output(latest)
                        print(json.dumps(data, indent=2)[:500] + "...")
                else:
                    print("No outputs found")

            elif choice == "3":
                report = self.create_exploration_report()
                print(report)

            elif choice == "4":
                storage = self.get_storage_usage()
                print(f"\nStorage Usage:")
                print(f"  Output: {storage['output_dir_mb']:.2f} MB")
                print(f"  Media: {storage['media_dir_mb']:.2f} MB")
                print(f"  Total: {storage['total_mb']:.2f} MB")

            elif choice == "5":
                concept = input("Enter concept name: ").strip()
                if concept:
                    package = self.package_exploration(concept)
                    print(f"Package created: {package}")

            elif choice == "6":
                keep = input("Keep how many recent files? (default: 10): ").strip()
                keep = int(keep) if keep.isdigit() else 10
                self.cleanup_old_outputs(keep)

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid option")


def main():
    """Main entry point for sandbox tools."""
    tools = SandboxTools()

    # Check if running interactively
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "report":
            tools.create_exploration_report()
        elif command == "storage":
            storage = tools.get_storage_usage()
            print(json.dumps(storage, indent=2))
        elif command == "menu":
            tools.interactive_menu()
        else:
            print(f"Unknown command: {command}")
    else:
        tools.interactive_menu()


if __name__ == "__main__":
    main()
