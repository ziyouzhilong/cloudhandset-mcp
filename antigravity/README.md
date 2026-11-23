# CloudHandset for Google Antigravity

[English](#english) · [简体中文](#简体中文)

## English

Use Antigravity to list the Android phones you rent from CloudHandset and request a screen check on a phone you choose. You need an active CloudHandset phone lease and a version of Antigravity with plugin support.

### Install

1. Download [the plugin ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/antigravity-v0.1.0/cloudhandset-antigravity-plugin-0.1.0.zip). The same release includes [SHA256SUMS](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/antigravity-v0.1.0/SHA256SUMS).
2. Extract the ZIP. Open a terminal in the directory **containing** the extracted `cloudhandset` folder and run:

   ```sh
   agy plugin install ./cloudhandset
   agy plugin list
   ```

   Look for `cloudhandset` version `0.1.0`. To install for just one project in the standalone IDE, place the entire folder at `.agents/plugins/cloudhandset/` in that project and reopen it.

### Sign in and try it

1. In **Customizations → Installed**, select **Authenticate** for the CloudHandset MCP server. In the CLI, open `/plugin`, expand **Installed → cloudhandset** and select **Sign in**.
2. Sign in on the CloudHandset verification page. Choose **Only one selected Android phone** for a single lease or **Current and future Android phone leases** for eligible phones on your account. If prompted, paste the code from Google's callback page into Antigravity's authorization field. Keep passwords and codes out of chat.
3. Ask **“List my CloudHandset phones.”** Choose a phone by the name returned. Then ask **“Show me the current screen on [phone name], describe it, and release control.”** Check the description and release result.

If the plugin is missing, check that you extracted the folder containing `plugin.json` and reopen the project. If the list is empty, check the signed-in account, active lease and selected authorization scope. An expired connection can be authorized again from Antigravity. For a global installation, uninstall with `agy plugin uninstall cloudhandset`. For a project installation, remove that project's plugin folder. Contact CloudHandset support to revoke server-side access.

## 简体中文

在 Antigravity 中可以列出你租用的 CloudHandset Android 手机，并指定一台查看屏幕。开始前，请准备有效的手机租约，并使用支持插件的 Antigravity 版本。

### 安装插件

1. 下载[插件 ZIP](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/antigravity-v0.1.0/cloudhandset-antigravity-plugin-0.1.0.zip)。同一版本也提供 [SHA256SUMS 校验文件](https://github.com/ziyouzhilong/cloudhandset-mcp/releases/download/antigravity-v0.1.0/SHA256SUMS)。
2. 解压 ZIP，在 **包含 `cloudhandset` 文件夹的上一级目录** 打开终端，运行以下命令。

   ```sh
   agy plugin install ./cloudhandset
   agy plugin list
   ```

   在列表中找到 `cloudhandset`，版本应为 `0.1.0`。使用独立 IDE 时，也可只为当前项目安装。将整个文件夹放到项目的 `.agents/plugins/cloudhandset/`，再重新打开该项目。

### 登录并使用

1. 在 **Customizations → Installed** 找到 CloudHandset 的 MCP 服务，点击 **Authenticate**。CLI 用户可输入 `/plugin`，展开 **Installed → cloudhandset**，选择 **Sign in**。
2. 在 CloudHandset 验证页登录。只连接一台手机时选 **Only one selected Android phone**。需要覆盖账户当前及未来的有效租约时选 **Current and future Android phone leases**。若 Google 回调页显示授权码，将其填回 Antigravity 的授权输入框。密码和授权码只在对应界面输入。
3. 先发送 **「列出我的 CloudHandset 手机」**。从返回的列表中选一台，再发送 **「查看［手机名称］的当前屏幕，描述画面后释放控制权」**。核对画面描述和释放结果。

如果看不到插件，请确认解压后的文件夹中包含 `plugin.json`，再重新打开项目。设备列表为空时，请核对登录账户、有效租约和本次授权范围。连接到期后可从 Antigravity 重新验证。全局安装可用 `agy plugin uninstall cloudhandset` 移除，项目安装则移除该项目的插件文件夹。如需撤销服务端访问权限，请联系 CloudHandset 客服。

[Google Antigravity plugins](https://antigravity.google/docs/plugins/) · [Google Antigravity MCP](https://antigravity.google/docs/mcp/)
