

---
description: '如何使用和运行来自 PowerApps-Samples 仓库的 PCF 样本组件'
applyTo: '**/*.{ts,tsx,js,json,xml,pcfproj,csproj}'
---

# 如何使用样本组件

本节列出的所有样本组件均可从 [github.com/microsoft/PowerApps-Samples/tree/master/component-framework](https://github.com/microsoft/PowerApps-Samples/tree/master/component-framework) 下载，以便您在模型驱动或画布应用中进行测试。

本节中的各个样本组件主题将为您提供样本组件的概述、其视觉外观以及完整的样本组件链接。

## 在尝试样本组件之前

要尝试样本组件，您必须首先：

- [下载](https://docs.github.com/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives-from-the-repository-view) 或 [克隆](https://docs.github.com/repositories/creating-and-managing-repositories/cloning-a-repository) 此仓库 [github.com/microsoft/PowerApps-Samples](https://github.com/microsoft/PowerApps-Samples)。
- 安装 [适用于 Windows 的 Power Platform CLI](https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction#install-power-platform-cli-for-windows)。

## 尝试样本组件

请遵循 [README.md](https://github.com/microsoft/PowerApps-Samples/blob/master/component-framework/README.md) 中的步骤，生成包含控件的解决方案，以便您可以在模型驱动或画布应用中导入并测试样本组件。

## 如何运行样本组件

使用以下步骤在您的模型驱动或画布应用中导入并测试样本组件。

### 分步操作流程

1. **下载或克隆仓库**
   - [下载](https://docs.github.com/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives-from-the-repository-view) 或 [克隆](https://docs.github.com/repositories/creating-and-managing-repositories/cloning-a-repository) [github.com/microsoft/PowerApps-Samples](https://github.com/microsoft/PowerApps-Samples)。

2. **打开开发者命令提示符**
   - 打开 [Visual Studio 的开发者命令提示符](https://learn.microsoft.com/visualstudio/ide/reference/command-prompt-powershell)，并导航到 `component-framework` 文件夹。
   - 在 Windows 上，您可以在“开始”菜单中输入 `developer command prompt` 来打开开发者命令提示符。

3. **安装依赖项**
   - 导航到您想要尝试的组件，例如 `IncrementControl`，并运行：
   ```bash
   npm install
   ```

4. **还原项目**
   - 在命令执行完成后，运行：
   ```bash
   msbuild /t:restore
   ```

5. **创建解决方案文件夹**
   - 在样本组件文件夹内创建一个新文件夹：
   ```bash
   mkdir IncrementControlSolution
   ```

6. **导航到解决方案文件夹**
   ```bash
   cd IncrementControlSolution
   ```

7. **初始化解决方案**
   - 在您创建的文件夹内运行 `pac solution init` 命令：
   ```bash
   pac solution init --publisher-name powerapps_samples --publisher-prefix sample
   ```
   > **注意**: 此命令会在该文件夹中创建一个名为 `IncrementControlSolution.cdsproj` 的新文件。

8. **添加组件引用**
   - 使用 `pac solution add-reference` 命令，并将 `path` 设置为 `.pcfproj` 文件的位置：
   ```bash
   pac solution add-reference --path ../../IncrementControl
   ```
   或
   ```bash
   pac solution add-reference --path ../../IncrementControl/IncrementControl.pcfproj
   ```
   > **重要**: 添加包含您要添加的控件的 `.pcfproj` 文件的文件夹作为引用。

9. **构建解决方案**
   - 要从您的解决方案项目生成 ZIP 文件，请运行以下三个命令：
   ```bash
   msbuild /t:restore
   msbuild /t:rebuild /restore /p:Configuration=Release
   msbuild
   ```
   - 生成的解决方案 ZIP 文件位于 `IncrementControlSolution\bin\debug` 文件夹中。

10. **导入解决方案**
    - 现在您已拥有 ZIP 文件，有两种选择：
      - 使用 [make.powerapps.com](https://make.powerapps.com/) 手动 [导入解决方案](https://learn.microsoft.com/powerapps/maker/data-platform/import-update-export-solutions) 到您的环境中。
      - 或者，使用 Power Apps CLI 命令导入解决方案，请参阅 [连接到您的环境](https://learn.microsoft.com/powerapps/developer/component-framework/import-custom-controls#connecting-to-your-environment) 和 [部署](https://learn.microsoft.com/powerapps/developer/component-framework/import-custom-controls#deploying-code-components) 部分。

11. **将组件添加到应用中**
    - 最后，要将代码组件添加到您的模型驱动和画布应用中，请参阅：
      - [将组件添加到模型驱动应用](https://learn.microsoft.com/powerapps/developer/component-framework/add-custom-controls-to-a-field-or-entity)
      - [将组件添加到画布应用](https://learn.microsoft.com/powerapps/developer/component-framework/component-framework-for-canvas-apps#add-components-to-a-canvas-app)

## 可用的样本组件

该仓库包含众多样本组件，包括：

- AngularJSFlipControl
- CanvasGridControl
- ChoicesPickerControl
- ChoicesPickerReactControl
- CodeInterpreterControl
- ControlStateAPI
- DataSetGrid
- DeviceApiControl
- FacepileReactControl
- FluentThemingAPIControl
- FormattingAPIControl
- IFrameControl
- ImageUploadControl
- IncrementControl
- LinearInputControl
- LocalizationAPIControl
- LookupSimpleControl
- MapControl
- ModelDrivenGridControl
- MultiSelectOptionSetControl
- NavigationAPIControl
- ObjectOutputControl
- PowerAppsGridCustomizerControl
- PropertySetTableControl
- ReactStandardControl
- TableControl
- TableGrid
- WebAPIControl

每个样本都展示了 Power Apps 组件框架的不同方面，可以作为学习资源或您自己组件的起点。