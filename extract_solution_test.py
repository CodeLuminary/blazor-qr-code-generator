import os
from extract_solution import extract_solution

llm_response = """
Okay, I will provide a Blazor Web App solution with ASP.NET Core that allows you to:

1.  Generate QR codes based on user input.
2.  Save the QR code images to a dynamically named folder.
3.  Display previously generated QR codes.
4.  Handle potential exceptions gracefully.

Here's the code, broken down into components and files:

**1. Project Setup**

Create a new Blazor Web App project in Visual Studio or using the .NET CLI.

```bash
dotnet new blazor -o QrCodeApp
cd QrCodeApp
```

**2. Dependencies**

Install the QRCoder package:

```bash
dotnet add package QRCoder
```

**3.  `QrCodeGenerator.razor` (Component for generating QR Codes)**

```csharp
// ./Components/Pages/QrCodeGenerator.razor
@page "/qrcode-generator"
@using QRCoder
@using System.IO
@inject IWebHostEnvironment Environment

<h3>QR Code Generator</h3>

<EditForm Model="@qrCodeModel" OnValidSubmit="@GenerateQrCode">
    <DataAnnotationsValidator />
    <ValidationSummary />

    <div class="form-group">
        <label for="QrCodeText">Text to encode:</label>
        <InputText id="QrCodeText" class="form-control" @bind-Value="qrCodeModel.QrCodeText" />
    </div>

    <div class="form-group">
        <label for="FolderName">Folder Name:</label>
        <InputText id="FolderName" class="form-control" @bind-Value="qrCodeModel.FolderName" />
    </div>

    <button type="submit" class="btn btn-primary">Generate QR Code</button>
</EditForm>

@if (!string.IsNullOrEmpty(qrCodeImageSrc))
{
    <h3>Generated QR Code:</h3>
    <img src="@qrCodeImageSrc" alt="QR Code" />
}

@code {
    private QrCodeModel qrCodeModel = new QrCodeModel();
    private string qrCodeImageSrc;

    public class QrCodeModel
    {
        [Required(ErrorMessage = "Text is required.")]
        public string QrCodeText { get; set; }

        [Required(ErrorMessage = "Folder Name is required.")]
        public string FolderName { get; set; }
    }

    private async Task GenerateQrCode()
    {
        try
        {
            string folderPath = Path.Combine(Environment.WebRootPath, "qrcodes", qrCodeModel.FolderName);

            // Ensure the directory exists
            if (!Directory.Exists(folderPath))
            {
                Directory.CreateDirectory(folderPath);
            }

            string fileName = $"{DateTime.Now.Ticks}.png"; // Use a unique filename
            string filePath = Path.Combine(folderPath, fileName);

            QRCodeGenerator qrGenerator = new QRCodeGenerator();
            QRCodeData qrCodeData = qrGenerator.CreateQrCode(qrCodeModel.QrCodeText, QRCodeGenerator.ECCLevel.Q);
            PngByteQRCode qrCode = new PngByteQRCode(qrCodeData);
            byte[] qrCodeAsPng = qrCode.GetPng(20);

            await File.WriteAllBytesAsync(filePath, qrCodeAsPng);

            qrCodeImageSrc = $"qrcodes/{qrCodeModel.FolderName}/{fileName}";
        }
        catch (Exception ex)
        {
            // Log the exception
            Console.Error.WriteLine($"Error generating QR code: {ex.Message}");
            // Optionally display an error message to the user
            qrCodeImageSrc = null; // Ensure no broken image is displayed
        }
    }
}
```

**4. `QrCodeDisplay.razor` (Component for displaying QR Codes)**

```csharp
// ./Components/Pages/QrCodeDisplay.razor
@page "/qrcode-display"
@inject IWebHostEnvironment Environment

<h3>Display QR Code</h3>

<div class="form-group">
    <label for="FolderName">Folder Name:</label>
    <InputText id="FolderName" class="form-control" @bind-Value="folderName" />
</div>

<div class="form-group">
    <label for="FileName">File Name:</label>
    <InputText id="FileName" class="form-control" @bind-Value="fileName" />
</div>

<button class="btn btn-primary" @onclick="DisplayQrCode">Display QR Code</button>

@if (!string.IsNullOrEmpty(qrCodeImageSrc))
{
    <img src="@qrCodeImageSrc" alt="QR Code" />
}

@code {
    private string folderName;
    private string fileName;
    private string qrCodeImageSrc;

    private void DisplayQrCode()
    {
        if (!string.IsNullOrEmpty(folderName) && !string.IsNullOrEmpty(fileName))
        {
            string imagePath = Path.Combine("qrcodes", folderName, fileName);
            string fullPath = Path.Combine(Environment.WebRootPath, imagePath);

            if (File.Exists(fullPath))
            {
                qrCodeImageSrc = imagePath;
            }
            else
            {
                qrCodeImageSrc = null;
                // Handle the case where the file doesn't exist (show an error message, etc.)
                Console.WriteLine("QR Code file not found.");
            }
        }
        else
        {
            qrCodeImageSrc = null;
            Console.WriteLine("Folder Name and File Name are required.");
            // Handle the case where folderName or fileName are empty
        }
    }
}
```

**5. `_Layout.razor` (or `MainLayout.razor`)**

Add navigation links to your layout to access the components:

```html
// ./Components/Layout/MainLayout.razor
@inherits LayoutComponentBase

<div class="page">
    <div class="sidebar">
        <NavMenu />
    </div>

    <main>
        <div class="top-row px-4">
            <a href="https://docs.microsoft.com/aspnet/" target="_blank">About</a>
        </div>

        <article class="content px-4">
            @Body
        </article>
    </main>
</div>
```

**6. `NavMenu.razor`**

Add links to the QR code generator and display pages.

```html
// ./Components/Layout/NavMenu.razor
<div class="top-row ps-3 navbar navbar-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="">QrCodeApp</a>
    </div>
</div>

<input class="navbar-toggler" type="checkbox" title="Navigation menu" aria-label="Toggle navigation" />

<div class="nav-scrollable" onclick="document.querySelector('.navbar-toggler').classList.toggle('collapsed')">
    <nav class="flex-column">
        <div class="nav-item px-3">
            <NavLink class="nav-link" href="/" Match="NavLinkMatch.All">
                <span class="oi oi-home" aria-hidden="true"></span> Home
            </NavLink>
        </div>

        <div class="nav-item px-3">
            <NavLink class="nav-link" href="/qrcode-generator">
                <span class="oi oi-plus" aria-hidden="true"></span> Generate QR Code
            </NavLink>
        </div>

        <div class="nav-item px-3">
            <NavLink class="nav-link" href="/qrcode-display">
                <span class="oi oi-list-rich" aria-hidden="true"></span> Display QR Code
            </NavLink>
        </div>
    </nav>
</div>
```

**7. Program.cs**

Register the `IWebHostEnvironment` service.  This is usually already done in a standard Blazor project, but double-check.

```csharp
// ./Program.cs
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using QrCodeApp;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("#headout");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
builder.Services.AddScoped<IWebHostEnvironment>(sp => sp.GetRequiredService<IWebAssemblyHostEnvironment>());

await builder.Build().RunAsync();
```

**Explanation:**

*   **`QrCodeGenerator.razor`**: This component handles the QR code generation.  It takes the text to encode and the folder name as input. It uses the `QRCoder` library to generate the QR code as a PNG byte array, then saves it to the specified folder with a unique filename (using the current timestamp).  The `qrCodeImageSrc` is then set to the relative path of the generated image.  Error handling is included within the `try...catch` block.
*   **`QrCodeDisplay.razor`**: This component displays a previously generated QR code.  It takes the folder name and file name as input.  It constructs the full path to the image, checks if the file exists, and then sets the `qrCodeImageSrc` to the relative path if the file is found.  It also includes basic error handling for missing files or empty input.
*   **Folder Structure:** The code saves the QR codes in the `wwwroot/qrcodes/{FolderName}` directory.  The `wwwroot` folder is the publicly accessible folder for static files in a Blazor application.
*   **Error Handling:**  `try...catch` blocks are used to handle potential exceptions during QR code generation and file access.  The exceptions are logged to the console, and you can extend the error handling to display user-friendly messages in the UI.
*   **Unique Filenames:** The generated QR code images are saved with unique filenames using the current timestamp (`DateTime.Now.Ticks`) to prevent naming conflicts.
*   **Data Binding and Validation:** The `EditForm`, `DataAnnotationsValidator`, `ValidationSummary`, and `InputText` components are used to handle user input, data binding, and validation.  The `QrCodeModel` class defines the properties and validation rules for the input fields.
*   **Relative Paths:** The `qrCodeImageSrc` variable stores the relative path to the QR code image, which is used in the `<img>` tag to display the image.  This ensures that the image can be accessed correctly from the browser.
*   **Dependency Injection:**  The `IWebHostEnvironment` interface is injected into the components to access the web root path.

**How to Run:**

1.  Build the project.
2.  Run the project.
3.  Navigate to `/qrcode-generator` to generate QR codes.
4.  Enter the text to encode and the folder name.
5.  Click "Generate QR Code."
6.  Navigate to `/qrcode-display` to display QR codes.
7.  Enter the folder name and file name of the QR code you want to display.
8.  Click "Display QR Code."

**Important Considerations:**

*   **Security:**  Be mindful of security implications when allowing users to specify folder names. Sanitize the input to prevent path traversal vulnerabilities.  Consider restricting the folder names to a predefined set of allowed values.
*   **Error Handling:** Implement more robust error handling to provide informative messages to the user.
*   **File Management:**  Implement a mechanism to manage the QR code files (e.g., deleting old files).
*   **UI Improvements:** Enhance the UI with progress indicators, error messages, and a more user-friendly design.
*   **Alternative Storage:**  Instead of storing the QR codes as files, you could store them in a database or cloud storage service.

This comprehensive example provides a solid foundation for building a QR code generation and display application with Blazor. Remember to adapt the code to your specific requirements and security considerations.

"""
try:
    response = extract_solution(llm_response=llm_response)

    if not isinstance(response, list):
        raise ValueError(
            "Expected response to be a list of (file_name, code) tuples.")

    for item in response:

        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("Invalid tuple.")

        file_name, code = item

        # Check if the file itself exists
        if not os.path.isfile(file_name):
            raise FileNotFoundError(
                f"The file '{file_name}' does not exist. Please check the path."
            )

        # Proceed to write only if the file already exists
        with open(file_name, "w") as file:
            file.write(code)

        print(f"File '{file_name}' written successfully.")

except FileNotFoundError as fnf_error:
    print(f"File error: {fnf_error}")

except Exception as e:
    print(f"An error occurred while running extract solution test: {e}")