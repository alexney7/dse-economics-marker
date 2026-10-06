# 发布到 GitHub（中文步骤）

本指南只指导发布，没有创建远程仓库或上传任何文件。先把本文件夹作为一个独立仓库；不要把整个 Codex 工作目录或 D 盘教学资料目录上传。

## 方式一：网页上传

1. 登录 GitHub，创建新仓库，名称可用 `dse-economics-marker`。首次可选 Private，检查内容后再决定是否公开。
2. 将提供的发布 ZIP 解压。进入能看到 `SKILL.md`、`README.md`、`references`、`scripts` 的那一层。
3. 在 GitHub 仓库选择 **Add file → Upload files**，上传这一层的文件及文件夹，确保根目录直接有 SKILL.md。网页上传不要只传 ZIP，否则只能下载压缩包，无法直接浏览 skill 结构。
4. 上传前查看文件列表。`.gitignore`、README、SKILL.md、依赖清单、references、scripts、agents、tests 可以上传。不要选择 `library.local.json`、PDF、图片、学生答卷或本地工作目录。
5. 提交说明可写 `Add DSE economics marking skill`，点击提交。完成后打开 SKILL.md 和 references，检查中文和链接。

注意：`.gitignore` 不会替网页上传过滤文件，所以优先使用已过滤的发布 ZIP。

## 方式二：Git 命令

在解压后的 skill 文件夹中打开 PowerShell。以下针对全新、独立仓库；不要在已有仓库里重复初始化或覆盖 origin。

```powershell
git init -b main
git add .gitignore SKILL.md README.md GITHUB-GUIDE.md requirements.txt agents references scripts tests VALIDATION.md
git status --short
git diff --cached --stat
```

确认暂存内容没有教材、试卷、答卷、个人路径配置。若 Git 要求身份，设置你的提交姓名及邮箱，可用 GitHub 提供的 noreply 邮箱：

```powershell
git config user.name "你的提交姓名"
git config user.email "你的GitHub提交邮箱"
git commit -m "Add DSE economics marking skill"
```

在 GitHub 新建空仓库；此方式不要勾选远程初始化 README，以避免两边各自出现初始提交。把下方 URL 替换成仓库页面给你的真实地址：

```powershell
git remote add origin https://github.com/YOUR-ACCOUNT/dse-economics-marker.git
git remote -v
git push -u origin main
```

按 Git 的认证提示登录，不把令牌写进文件或远程 URL。若仓库已包含 README／其他提交，先克隆该仓库，再将 skill 文件复制进去提交，不强制推送。

## 后续更新

修改 SKILL.md 或 references 后，先试批已有答案并检查差异。确认变化后提交选定文件再 push。教师一次裁定不应自动变成通用规则；需要明确适用范围。

新年份的真题仍留本地，通过对话提供路径，或更新索引的相对路径。GitHub 下载者需要自行提供其可用的题目、评分参考和教材；上传 skill 并不会上传你的知识材料，也不等于完成模型训练。

## 官方操作参考

- [GitHub：将本地代码添加到 GitHub](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
- [GitHub：上传文件](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)

发布 ZIP 不含本机配置、PDF、图片及批改记录。它没有替你选择开源许可证；可在确定使用和分享方式后添加 LICENSE。
