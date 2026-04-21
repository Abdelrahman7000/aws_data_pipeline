# This is the main Terraform configuration file that orchestrates the deployment of the VPC, IAM, Storage, and Compute modules.

module "vpc" {
  source = "./modules/vpc"
}

module "iam" {
  source = "./modules/iam"
}

module "storage" {
  source = "./modules/storage"
}

module "compute" {
  source = "./modules/compute"

  # from VPC module
  subnet_id = module.vpc.public_subnet_id
  master_sg = module.vpc.master_sg
  core_sg   = module.vpc.core_sg

  # from IAM module
  lambda_role_arn        = module.iam.lambda_role_arn
  service_role_arn       = module.iam.emr_service_role_arn
  instance_profile_arn   = module.iam.emr_instance_profile_arn

  # from Storage module
  bucket_name = module.storage.bucket_name
}