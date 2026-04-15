# # create a VPC and subnet for the Glue Connection to access the on-prem SQL Server
# resource "aws_vpc" "main" {
#   cidr_block = "10.0.0.0/16"
#   tags = {
#     Name = "my-etl-vpc"
#   }
# }

# resource "aws_internet_gateway" "igw" {
#   vpc_id = aws_vpc.main.id

#   tags = {
#     Name = "my-etl-igw"
#   }
# }


# resource "aws_subnet" "public" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = "10.0.1.0/24"
#   availability_zone = "us-east-1a" # Must match the Glue Connection AZ
#   map_public_ip_on_launch = true
#    tags = {
#     Name = "public-subnet-for-etl"
#   }
# }

# resource "aws_subnet" "private" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = "10.0.2.0/24"
#   availability_zone = "us-east-1a"

#   tags = {
#     Name = "private-subnet-for-etl"
#   }
# }

# # Create a Route Table for the public subnet to allow internet access
# resource "aws_route_table" "public" {
#   vpc_id = aws_vpc.main.id

#   tags = {
#     Name = "public-rt-for-etl"
#   }
# }
# # Add a default route to the Internet Gateway for the public route table
# resource "aws_route" "public_internet" {
#   route_table_id         = aws_route_table.public.id
#   destination_cidr_block = "0.0.0.0/0"
#   gateway_id             = aws_internet_gateway.igw.id
# }
# # 
# resource "aws_route_table_association" "public_assoc" {
#   subnet_id      = aws_subnet.public.id
#   route_table_id = aws_route_table.public.id
# }

# #  Private Route Table 
# resource "aws_route_table" "private" {
#   vpc_id = aws_vpc.main.id

#   tags = {
#     Name = "private-rt-for-etl"
#   }
# }

# resource "aws_route_table_association" "private_assoc" {
#   subnet_id      = aws_subnet.private.id
#   route_table_id = aws_route_table.private.id
# }



# resource "aws_vpc_endpoint" "s3" {
#   vpc_id       = aws_vpc.main.id
#   service_name = "com.amazonaws.us-east-1.s3"
#   vpc_endpoint_type = "Gateway"

#   route_table_ids = [
#     aws_route_table.private.id,
#     aws_route_table.public.id
#   ]

#   tags = {
#     Name = "s3-endpoint"
#   }
# }


#######################################################################

# resource "aws_security_group" "glue_sg" {
#   name   = "glue-on-prem-access"
#   vpc_id = aws_vpc.main.id

#   # Rule 1: Allow Glue to talk to itself (Required for Glue ETL)
#   ingress {
#     from_port = 0
#     to_port   = 65535
#     protocol  = "tcp"
#     self      = true
#   } 

#   egress {
#     from_port = 0
#     to_port   = 65535
#     protocol  = "tcp"
#     self      = true
#   }
  
#   # Rule 2: Allow outbound to your SQL Server
#   egress {
#     from_port   = 1433
#     to_port     = 1433
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"] # The IP range of your on-prem network
#   }
# }



# # 2. Associate it with your subnet
# resource "aws_route_table_association" "private_assoc" {
#   subnet_id      = aws_subnet.private_subnet.id
#   route_table_id = aws_route_table.private.id
# }

# # Create a VPC Endpoint for S3 to allow Glue to access S3 without going through the internet
# resource "aws_vpc_endpoint" "s3" {
#   vpc_id       = aws_vpc.main.id
#   service_name = "com.amazonaws.us-east-1.s3" 
# }

# # 3. Connect the S3 Endpoint to that Route Table
# resource "aws_vpc_endpoint_route_table_association" "s3_access" {
#   route_table_id  = aws_route_table.private.id
#   vpc_endpoint_id = aws_vpc_endpoint.s3.id
# }