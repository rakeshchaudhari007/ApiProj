-- Step 1: Create Users Table
CREATE TABLE Users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(100) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    email NVARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT GETDATE()
);

-- Step 2: Create Resources Table
CREATE TABLE Resources (
    id INT PRIMARY KEY IDENTITY(1,1),
    resource_name NVARCHAR(255) NOT NULL,
    resource_type NVARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- Step 3: Create Subnets Table
CREATE TABLE Subnets (
    id INT PRIMARY KEY IDENTITY(1,1),
    subnet_name NVARCHAR(255) NOT NULL,
    subnet_address NVARCHAR(50) NOT NULL,
    vnet_name NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
