"""
Project Validation Script for APIGatewayPOC
Verifies all required files exist and are properly configured
"""
import os
import sys
from pathlib import Path

class ProjectValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
        
    def check_file_exists(self, filepath, required=True):
        """Check if a file exists"""
        if os.path.exists(filepath):
            print(f"? {filepath}")
            self.success_count += 1
            return True
        else:
            msg = f"? Missing: {filepath}"
            if required:
                self.errors.append(msg)
            else:
                self.warnings.append(msg)
            print(msg)
            return False
    
    def check_directory_exists(self, dirpath):
        """Check if a directory exists"""
        if os.path.isdir(dirpath):
            print(f"? {dirpath}/")
            self.success_count += 1
            return True
        else:
            msg = f"? Missing directory: {dirpath}/"
            self.errors.append(msg)
            print(msg)
            return False
    
    def validate_structure(self):
        """Validate the project structure"""
        print("=" * 60)
        print("PROJECT STRUCTURE VALIDATION")
        print("=" * 60)
        
        # Root files
        print("\n?? Root Configuration Files:")
        self.check_file_exists("README.md")
        self.check_file_exists("docker-compose.yml")
        self.check_file_exists(".gitignore")
        self.check_file_exists(".copilot-instructions.md")
        
        # Service directories
        print("\n?? Service Directories:")
        self.check_directory_exists("services")
        self.check_directory_exists("services/gateway")
        self.check_directory_exists("services/customer-service")
        self.check_directory_exists("services/product-service")
        self.check_directory_exists("services/shared")
        
        # Gateway files
        print("\n?? Gateway (Envoy) Files:")
        self.check_file_exists("services/gateway/Dockerfile")
        self.check_file_exists("services/gateway/envoy.yaml")
        
        # Customer Service files
        print("\n?? Customer Service Files:")
        self.check_file_exists("services/customer-service/Dockerfile")
        self.check_file_exists("services/customer-service/main.py")
        self.check_file_exists("services/customer-service/requirements.txt")
        self.check_file_exists("services/customer-service/models/customer.py")
        self.check_file_exists("services/customer-service/models/__init__.py")
        
        # Product Service files
        print("\n?? Product Service Files:")
        self.check_file_exists("services/product-service/Dockerfile")
        self.check_file_exists("services/product-service/main.py")
        self.check_file_exists("services/product-service/requirements.txt")
        self.check_file_exists("services/product-service/models/product.py")
        self.check_file_exists("services/product-service/models/__init__.py")
        
        # Shared utilities
        print("\n?? Shared Utilities:")
        self.check_file_exists("services/shared/common.py")
        self.check_file_exists("services/shared/__init__.py")
        
        # Test files
        print("\n?? Test Files:")
        self.check_directory_exists("tests")
        self.check_file_exists("tests/__init__.py")
        self.check_file_exists("tests/requirements.txt")
        self.check_file_exists("tests/test_customer_service.py")
        self.check_file_exists("tests/test_product_service.py")
        self.check_file_exists("tests/integration/test_api_gateway.py")
        self.check_file_exists("tests/integration/__init__.py")
        
        # Scripts
        print("\n?? Helper Scripts:")
        self.check_directory_exists("scripts")
        self.check_file_exists("scripts/setup.sh")
        self.check_file_exists("scripts/start.sh")
        self.check_file_exists("scripts/stop.sh")
        self.check_file_exists("scripts/test.sh")
    
    def validate_docker_files(self):
        """Validate Docker configuration"""
        print("\n" + "=" * 60)
        print("DOCKER CONFIGURATION VALIDATION")
        print("=" * 60)
        
        # Check docker-compose.yml syntax
        print("\n?? Docker Compose Configuration:")
        try:
            import subprocess
            result = subprocess.run(
                ["docker-compose", "config", "--quiet"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("? docker-compose.yml is valid")
                self.success_count += 1
            else:
                msg = f"? docker-compose.yml has errors: {result.stderr}"
                self.errors.append(msg)
                print(msg)
        except Exception as e:
            msg = f"??  Could not validate docker-compose.yml: {e}"
            self.warnings.append(msg)
            print(msg)
    
    def check_gitignore(self):
        """Check if .gitignore contains essential patterns"""
        print("\n" + "=" * 60)
        print("GITIGNORE VALIDATION")
        print("=" * 60)
        
        essential_patterns = [
            "__pycache__",
            "*.pyc",
            ".env",
            ".vscode",
            ".vs",
            "*.log"
        ]
        
        if os.path.exists(".gitignore"):
            with open(".gitignore", "r") as f:
                content = f.read()
            
            print("\n?? Checking essential patterns:")
            for pattern in essential_patterns:
                if pattern in content:
                    print(f"? {pattern}")
                    self.success_count += 1
                else:
                    msg = f"??  Missing pattern: {pattern}"
                    self.warnings.append(msg)
                    print(msg)
        else:
            msg = "? .gitignore file not found"
            self.errors.append(msg)
            print(msg)
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        
        print(f"\n? Successful checks: {self.success_count}")
        
        if self.warnings:
            print(f"\n??  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   {warning}")
        
        if self.errors:
            print(f"\n? Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   {error}")
            print("\n? VALIDATION FAILED - Please fix the errors above")
            return False
        else:
            print("\n?? VALIDATION PASSED - All required files are present and configured correctly!")
            return True

def main():
    validator = ProjectValidator()
    
    print("\n" + "=" * 60)
    print("APIGatewayPOC - Project Validation")
    print("=" * 60)
    
    # Run all validations
    validator.validate_structure()
    validator.validate_docker_files()
    validator.check_gitignore()
    
    # Print summary
    success = validator.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()