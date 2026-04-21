output "public_subnet_id" {
  value = aws_subnet.public_subnet.id
}
 
output "master_sg" {
  value = aws_security_group.public_sg.id
}

output "core_sg" {
  value = aws_security_group.public_sg_2.id
}

output "vpc_id" {
  value = aws_vpc.my_vpc.id
}