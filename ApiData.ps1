
$baseUrl = 'https://.centralindia-01.azurewebsites.net'
# 2. register
$registerurl = "$baseUrl/register"
$registerdata = @{
    username = "testuser"
    password = "password123"
    email = 'test@m.com'
}

# Convert to JSON and send the POST request for login
$registerJson = $registerdata | ConvertTo-Json
$loginResponse = Invoke-RestMethod -Uri $loginUrl -Method Post -Body $registerJson -ContentType "application/json" -SessionVariable session

# 2. Login with the same user
$loginUrl = "$baseUrl/login"
$loginData = @{
    username = "testuser"
    password = "password123"
}

# Convert to JSON and send the POST request for login
$loginJson = $loginData | ConvertTo-Json
$loginResponse = Invoke-RestMethod -Uri $loginUrl -Method Post -Body $loginJson -ContentType "application/json" -SessionVariable session

# Check if login was successful
if ($loginResponse.message -eq "Login successful!") {
    Write-Host "Login successful!"

    # 3. Create VNet and Subnets
    $createVNetUrl = "$baseUrl/create_vnet"
    $vnetData = @{
        vnet_name = "apivnet-new"
        resource_group = "apivnetrg-new"
        location = "central India"
        "address_space" = "192.0.0.0/16"
        subnets = @(
            @{
                subnet_name = "subnet223"
                subnet_address = "192.0.6.0/24"
            },
            @{
                subnet_name = "subnet221"
                subnet_address = "192.0.7.0/24"
            }
        )
    }

    # Convert to JSON and send the POST request for VNet creation
    $vnetJson = $vnetData | ConvertTo-Json -Depth 3
    $vnetResponse = Invoke-RestMethod -Uri $createVNetUrl -Method Post -Body $vnetJson -ContentType "application/json" -WebSession $session

    Write-Host "VNet Creation Response: $($vnetResponse.message)"
} else {
    Write-Host "Login failed: $($loginResponse.error)"
}
