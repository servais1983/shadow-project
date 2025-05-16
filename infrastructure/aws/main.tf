provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "La région AWS où déployer"
  default     = "eu-west-3"
}

variable "app_name" {
  description = "Nom de l'application"
  default     = "shadow"
}

variable "environment" {
  description = "Environnement de déploiement"
  default     = "prod"
}

# VPC et sous-réseaux
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "${var.app_name}-vpc-${var.environment}"
  }
}

resource "aws_subnet" "public_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  
  tags = {
    Name = "${var.app_name}-public-subnet-1-${var.environment}"
  }
}

resource "aws_subnet" "public_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.aws_region}b"
  
  tags = {
    Name = "${var.app_name}-public-subnet-2-${var.environment}"
  }
}

# Base de données RDS PostgreSQL
resource "aws_db_subnet_group" "main" {
  name       = "${var.app_name}-db-subnet-group-${var.environment}"
  subnet_ids = [aws_subnet.public_1.id, aws_subnet.public_2.id]
  
  tags = {
    Name = "${var.app_name}-db-subnet-group-${var.environment}"
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "14"
  instance_class       = "db.t3.micro"
  db_name              = "shadow"
  username             = "shadow_admin"
  password             = var.db_password
  db_subnet_group_name = aws_db_subnet_group.main.name
  skip_final_snapshot  = true
  
  tags = {
    Name = "${var.app_name}-db-${var.environment}"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.app_name}-cluster-${var.environment}"
  
  tags = {
    Name = "${var.app_name}-cluster-${var.environment}"
  }
}

# Variables sensibles
variable "db_password" {
  description = "Mot de passe pour la base de données PostgreSQL"
  type        = string
  sensitive   = true
}
