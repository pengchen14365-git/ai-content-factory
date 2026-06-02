module.exports = async (params) => {
    const app = params.app;
    const quickAddApi = params.quickAddApi;

    // 1. 弹出输入框，让用户输入稿件标题
    const 稿件标题 = await quickAddApi.inputPrompt("请输入稿件标题");
    if (!稿件标题) {
        new Notice("稿件标题不能为空！");
        return;
    }

    // 2. 生成日期后缀，规范文件夹命名
    const 日期 = moment().format("YYYYMMDD");
    const 文件夹名称 = `${稿件标题}-${日期}`;
    const 文件夹路径 = `02-稿件库/01-创作中稿件/${文件夹名称}`;

    // 3. 创建稿件根文件夹和assets图片文件夹
    try { await app.vault.createFolder(文件夹路径); } catch(e) {}
    try { await app.vault.createFolder(`${文件夹路径}/assets`); } catch(e) {}

    // 4. 读取访谈记录模板
    let 访谈模板内容 = "";
    const 模板文件 = app.vault.getAbstractFileByPath("00-模板库/模板-访谈记录.md");
    if (模板文件) {
        访谈模板内容 = await app.vault.read(模板文件);
        访谈模板内容 = 访谈模板内容
            .replace(/\{\{NAME\}\}/g, 稿件标题)
            .replace(/\{\{DATE:YYYY-MM-DD\}\}/g, moment().format("YYYY-MM-DD"));
    }

    // 5. 创建所有笔记文件
    const 待创建文件列表 = [];
    if (访谈模板内容) {
        待创建文件列表.push({ 文件名: "访谈记录.md", 内容: 访谈模板内容 });
    }

    // 补充其他稿件必备文件（无模板则生成空白占位文件）
    const 标准文件 = [
        "初稿.md",
        "修改稿.md",
        "终稿.md",
        "发布信息.md"
    ];
    标准文件.forEach(文件名 => 待创建文件列表.push({ 文件名, 内容: "" }));

    // 6. 逐个写入文件
    for (const 文件 of 待创建文件列表) {
        const 文件路径 = `${文件夹路径}/${文件.文件名}`;
        try {
            const 已存在 = app.vault.getAbstractFileByPath(文件路径);
            if (!已存在) {
                await app.vault.create(文件路径, 文件.内容);
            }
        } catch(e) {
            // 文件已存在则跳过
        }
    }

    // 7. 通知用户创建完成
    new Notice(`✅ 稿件文件夹已创建：${文件夹名称}`);
};
