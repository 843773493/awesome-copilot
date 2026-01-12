

---
description: '全面的Power BI自定义可视化开发指南，涵盖React、D3.js集成、TypeScript模式、测试框架和高级可视化技术。'
applyTo: '**/*.{ts,tsx,js,jsx,json,less,css}'
---

# Power BI自定义可视化开发最佳实践

## 概述
本文档提供了使用现代网络技术（包括React、D3.js、TypeScript和高级测试框架）开发自定义Power BI可视化的全面指导，基于微软官方指导和社区最佳实践。

## 开发环境设置

### 1. 项目初始化
```typescript
// 全局安装Power BI可视化工具
npm install -g powerbi-visuals-tools

// 创建新可视化项目
pbiviz new MyCustomVisual
cd MyCustomVisual

// 启动开发服务器
pbiviz start
```

### 2. TypeScript配置
```json
{
    "compilerOptions": {
        "jsx": "react",
        "types": ["react", "react-dom"],
        "allowJs": false,
        "emitDecoratorMetadata": true,
        "experimentalDecorators": true,
        "target": "es6",
        "sourceMap": true,
        "outDir": "./.tmp/build/",
        "moduleResolution": "node",
        "declaration": true,
        "lib": [
            "es2015",
            "dom"
        ]
    },
    "files": [
        "./src/visual.ts"
    ]
}
```

## 核心可视化开发模式

### 1. 基础可视化结构
```typescript
"use strict";
import powerbi from "powerbi-visuals-api";

import DataView = powerbi.DataView;
import VisualConstructorOptions = powerbi.extensibility.visual.VisualConstructorOptions;
import VisualUpdateOptions = powerbi.extensibility.visual.VisualUpdateOptions;
import IVisual = powerbi.extensibility.visual.IVisual;
import IVisualHost = powerbi.extensibility.IVisualHost;

import "./../style/visual.less";

export class Visual implements IVisual {
    private target: HTMLElement;
    private host: IVisualHost;

    constructor(options: VisualConstructorOptions) {
        this.target = options.element;
        this.host = options.host;
    }

    public update(options: VisualUpdateOptions) {
        const dataView: DataView = options.dataViews[0];
        
        if (!dataView) {
            return;
        }

        // 可视化更新逻辑
    }

    public getFormattingModel(): powerbi.visuals.FormattingModel {
        return this.formattingSettingsService.buildFormattingModel(this.formattingSettings);
    }
}
```

### 2. 数据视图处理
```typescript
// 单数据映射示例
export class Visual implements IVisual {
    private valueText: HTMLParagraphElement;

    constructor(options: VisualConstructorOptions) {
        this.target = options.element;
        this.host = options.host;
        this.valueText = document.createElement("p");
        this.target.appendChild(this.valueText);
    }

    public update(options: VisualUpdateOptions) {
        const dataView: DataView = options.dataViews[0];
        const singleDataView: DataViewSingle = dataView.single;

        if (!singleDataView || !singleDataView.value ) {
            return;
        }

        this.valueText.innerText = singleDataView.value.toString();
    }
}
```

## React集成

### 1. React可视化设置
```typescript
import * as React from "react";
import * as ReactDOM from "react-dom";
import ReactCircleCard from "./component";

export class Visual implements IVisual {
    private target: HTMLElement;
    private reactRoot: React.ComponentElement<any, any>;

    constructor(options: VisualConstructorOptions) {
        this.reactRoot = React.createElement(ReactCircleCard, {});
        this.target = options.element;

        ReactDOM.render(this.reactRoot, this.target);
    }

    public update(options: VisualUpdateOptions) {
        const dataView = options.dataViews[0];
        
        if (dataView) {
            const reactProps = this.parseDataView(dataView);
            this.reactRoot = React.createElement(ReactCircleCard, reactProps);
            ReactDOM.render(this.reactRoot, this.target);
        }
    }

    private parseDataView(dataView: DataView): any {
        // 将Power BI数据转换为React组件格式
        return {
            data: dataView.categorical?.values?.[0]?.values || [],
            categories: dataView.categorical?.categories?.[0]?.values || []
        };
    }
}
```

### 2. 带有属性的React组件
```typescript
// Power BI可视化的React组件
import * as React from "react";

export interface ReactCircleCardProps {
    data: number[];
    categories: string[];
    size?: number;
    color?: string;
}

export const ReactCircleCard: React.FC<ReactCircleCardProps> = (props) => {
    const { data, categories, size = 200, color = "#3498db" } = props;
    
    const maxValue = Math.max(...data);
    const minValue = Math.min(...data);
    
    return (
        <div className="react-circle-card">
            {data.map((value, index) => {
                const radius = ((value - minValue) / (maxValue - minValue)) * size / 2;
                return (
                    <div key={index} className="data-point">
                        <div 
                            className="circle"
                            style={{
                                width: radius * 2,
                                height: radius * 2,
                                backgroundColor: color,
                                borderRadius: '50%'
                            }}
                        />
                        <span className="label">{categories[index]}: {value}</span>
                    </div>
                );
            })}
        </div>
    );
};

export default ReactCircleCard;
```

## D3.js集成

### 1. D3与TypeScript
```typescript
import * as d3 from "d3";
type Selection<T extends d3.BaseType> = d3.Selection<T, any, any, any>;

export class Visual implements IVisual {
    private svg: Selection<SVGElement>;
    private container: Selection<SVGElement>;
    private host: IVisualHost;

    constructor(options: VisualConstructorOptions) {
        this.host = options.host;
        this.svg = d3.select(options.element)
            .append('svg')
            .classed('visual-svg', true);
        
        this.container = this.svg
            .append('g')
            .classed('visual-container', true);
    }

    public update(options: VisualUpdateOptions) {
        const dataView = options.dataViews[0];
        
        if (!dataView) {
            return;
        }

        const width = options.viewport.width;
        const height = options.viewport.height;
        
        this.svg
            .attr('width', width)
            .attr('height', height);

        // D3数据绑定和可视化逻辑
        this.renderChart(dataView, width, height);
    }

    private renderChart(dataView: DataView, width: number, height: number): void {
        const data = this.transformData(dataView);
        
        // 创建比例尺
        const xScale = d3.scaleBand()
            .domain(data.map(d => d.category))
            .range([0, width])
            .padding(0.1);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
            .range([height, 0]);

        // 绑定数据并创建条形图
        const bars = this.container.selectAll('.bar')
            .data(data);

        bars.enter()
            .append('rect')
            .classed('bar', true)
            .merge(bars)
            .attr('x', d => xScale(d.category))
            .attr('y', d => yScale(d.value))
            .attr('width', xScale.bandwidth())
            .attr('height', d => height - yScale(d.value))
            .style('fill', '#3498db');

        bars.exit().remove();
    }

    private transformData(dataView: DataView): any[] {
        // 将Power BI DataView转换为D3友好格式
        const categorical = dataView.categorical;
        const categories = categorical.categories[0];
        const values = categorical.values[0];

        return categories.values.map((category, index) => ({
            category: category.toString(),
            value: values.values[index] as number
        }));
    }
}
```

### 2. 高级D3模式
```typescript
// 带有交互功能的复杂D3可视化
export class AdvancedD3Visual implements IVisual {
    private svg: Selection<SVGElement>;
    private tooltip: Selection<HTMLDivElement>;
    private selectionManager: ISelectionManager;

    constructor(options: VisualConstructorOptions) {
        this.host = options.host;
        this.selectionManager = this.host.createSelectionManager();
        
        // 创建主SVG
        this.svg = d3.select(options.element)
            .append('svg');
        
        // 创建提示框
        this.tooltip = d3.select(options.element)
            .append('div')
            .classed('tooltip', true)
            .style('opacity', 0);
    }

    private createInteractiveElements(data: VisualDataPoint[]): void {
        const circles = this.svg.selectAll('.data-circle')
            .data(data);

        const circlesEnter = circles.enter()
            .append('circle')
            .classed('data-circle', true);

        circlesEnter.merge(circles)
            .attr('cx', d => d.x)
            .attr('cy', d => d.y)
            .attr('r', d => d.radius)
            .style('fill', d => d.color)
            .style('stroke', d => d.strokeColor)
            .style('stroke-width', d => `${d.strokeWidth}px`)
            .on('click', (event, d) => {
                // 处理选择
                this.selectionManager.select(d.selectionId, event.ctrlKey);
            })
            .on('mouseover', (event, d) => {
                // 显示提示框
                this.tooltip
                    .style('opacity', 1)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 10) + 'px')
                    .html(`${d.category}: ${d.value}`);
            })
            .on('mouseout', () => {
                // 隐藏提示框
                this.tooltip.style('opacity', 0);
            });

        circles.exit().remove();
    }
}
```

## 高级可视化功能

### 1. 自定义格式化模型
```typescript
import { formattingSettings } from "powerbi-visuals-utils-formattingmodel";

export class VisualFormattingSettingsModel extends formattingSettings.CompositeFormattingSettingsModel {
    // 颜色设置卡
    public colorCard: ColorCardSettings = new ColorCardSettings();
    
    // 数据点设置卡  
    public dataPointCard: DataPointCardSettings = new DataPointCardSettings();
    
    // 通用设置卡
    public generalCard: GeneralCardSettings = new GeneralCardSettings();

    public cards: formattingSettings.SimpleCard[] = [this.colorCard, this.dataPointCard, this.generalCard];
}

export class ColorCardSettings extends formattingSettings.SimpleCard {
    name: string = "colorCard";
    displayName: string = "颜色";

    public defaultColor: formattingSettings.ColorPicker = new formattingSettings.ColorPicker({
        name: "defaultColor",
        displayName: "默认颜色",
        value: { value: "#3498db" }
    });

    public showAllDataPoints: formattingSettings.ToggleSwitch = new formattingSettings.ToggleSwitch({
        name: "showAllDataPoints",
        displayName: "全部显示",
        value: false
    });
}
```

### 2. 交互性与选择
```typescript
import { interactivitySelectionService, baseBehavior } from "powerbi-visuals-utils-interactivityutils";

export interface VisualDataPoint extends interactivitySelectionService.SelectableDataPoint {
    value: powerbi.PrimitiveValue;
    category: string;
    color: string;
    selectionId: ISelectionId;
}

export class VisualBehavior extends baseBehavior.BaseBehavior<VisualDataPoint> {
    protected bindClick() {
        // 实现数据点选择的点击行为
        this.behaviorOptions.clearCatcher.on('click', () => {
            this.selectionHandler.handleClearSelection();
        });

        this.behaviorOptions.elementsSelection.on('click', (event, dataPoint) => {
            event.stopPropagation();
            this.selectionHandler.handleSelection(dataPoint, event.ctrlKey);
        });
    }

    protected bindContextMenu() {
        // 实现上下文菜单行为
        this.behaviorOptions.elementsSelection.on('contextmenu', (event, dataPoint) => {
            this.selectionHandler.handleContextMenu(
                dataPoint ? dataPoint.selectionId : null,
                {
                    x: event.clientX,
                    y: event.clientY
                }
            );
            event.preventDefault();
        });
    }
}
```

### 3. 主页实现
```typescript
export class Visual implements IVisual {
    private element: HTMLElement;
    private isLandingPageOn: boolean;
    private LandingPageRemoved: boolean;
    private LandingPage: d3.Selection<any>;

    constructor(options: VisualConstructorOptions) {
        this.element = options.element;
    }

    public update(options: VisualUpdateOptions) {
        this.HandleLandingPage(options);
    }

    private HandleLandingPage(options: VisualUpdateOptions) {
        if(!options.dataViews || !options.dataViews[0]?.metadata?.columns?.length){
            if(!this.isLandingPageOn) {
                this.isLandingPageOn = true;
                const SampleLandingPage: Element = this.createSampleLandingPage();
                this.element.appendChild(SampleLandingPage);
                this.LandingPage = d3.select(SampleLandingPage);
            }
        } else {
            if(this.isLandingPageOn && !this.LandingPageRemoved){
                this.LandingPageRemoved = true;
                this.LandingPage.remove();
            }
        }
    }

    private createSampleLandingPage(): Element {
        const landingPage = document.createElement("div");
        landingPage.className = "landing-page";
        landingPage.innerHTML = `
            <div class="landing-page-content">
                <h2>自定义可视化</h2>
                <p>添加数据以开始</p>
                <div class="landing-page-icon">📊</div>
            </div>
        `;
        return landingPage;
    }
}
```

## 测试框架

### 1. 单元测试设置
```typescript
// 用于测试的Webpack配置
const path = require('path');
const webpack = require("webpack");

module.exports = {
    devtool: 'source-map',
    mode: 'development',
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/
            },
            {
                test: /\.json$/,
                loader: 'json-loader'
            },
            {
                test: /\.tsx?$/i,
                enforce: 'post',
                include: path.resolve(__dirname, 'src'),
                exclude: /(node_modules|resources\/js\/vendor)/,
                loader: 'coverage-istanbul-loader',
                options: { esModules: true }
            }
        ]
    },
    externals: {
        "powerbi-visuals-api": '{}'
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js', '.css']
    },
    output: {
        path: path.resolve(__dirname, ".tmp/test")
    },
    plugins: [
        new webpack.ProvidePlugin({
            'powerbi-visuals-api': null
        })
    ]
};
```

### 2. 可视化测试工具
```typescript
// Power BI可视化的测试工具
export class VisualTestUtils {
    public static d3Click(element: JQuery, x: number, y: number): void {
        const event = new MouseEvent('click', {
            clientX: x,
            clientY: y,
            button: 0
        });
        element[0].dispatchEvent(event);
    }

    public static d3KeyEvent(element: JQuery, typeArg: string, keyArg: string, keyCode: number): void {
        const event = new KeyboardEvent(typeArg, {
            key: keyArg,
            code: keyArg,
            keyCode: keyCode
        });
        element[0].dispatchEvent(event);
    }

    public static createVisualHost(): IVisualHost {
        return {
            createSelectionIdBuilder: () => new SelectionIdBuilder(),
            createSelectionManager: () => new SelectionManager(),
            colorPalette: new ColorPalette(),
            eventService: new EventService(),
            tooltipService: new TooltipService()
        } as IVisualHost;
    }

    public static createUpdateOptions(dataView: DataView, viewport?: IViewport): VisualUpdateOptions {
        return {
            dataViews: [dataView],
            viewport: viewport || { width: 500, height: 500 },
            operationKind: VisualDataChangeOperationKind.Create,
            type: VisualUpdateType.Data
        };
    }
}
```

### 3. 组件测试
```typescript
// Jest测试React组件
import * as React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ReactCircleCard from '../src/component';

describe('ReactCircleCard', () => {
    const mockProps = {
        data: [10, 20, 30],
        categories: ['A', 'B', 'C'],
        size: 200,
        color: '#3498db'
    };

    test('渲染具有正确数据点', () => {
        render(<ReactCircleCard {...mockProps} />);
        
        expect(screen.getByText('A: 10')).toBeInTheDocument();
        expect(screen.getByText('B: 20')).toBeInTheDocument();
        expect(screen.getByText('C: 30')).toBeInTheDocument();
    });

    test('应用正确样式', () => {
        render(<ReactCircleCard {...mockProps} />);
        
        const circles = document.querySelectorAll('.circle');
        expect(circles).toHaveLength(3);
        
        circles.forEach(circle => {
            expect(circle).toHaveStyle('backgroundColor: #3498db');
            expect(circle).toHaveStyle('borderRadius: 50%');
        });
    });

    test('优雅处理空数据', () => {
        const emptyProps = { ...mockProps, data: [], categories: [] };
        const { container } = render(<ReactCircleCard {...emptyProps} />);
        
        expect(container.querySelector('.data-point')).toBeNull();
    });
});
```

## 高级模式

### 1. 对话框实现
```typescript
import DialogConstructorOptions = powerbi.extensibility.visual.DialogConstructorOptions;
import DialogAction = powerbi.DialogAction;
import * as ReactDOM from 'react-dom';
import * as React from 'react';

export class CustomDialog {
    private dialogContainer: HTMLElement;

    constructor(options: DialogConstructorOptions) {
        this.dialogContainer = options.element;
        this.initializeDialog();
    }

    private initializeDialog(): void {
        const dialogContent = React.createElement(DialogContent, {
            onSave: this.handleSave.bind(this),
            onCancel: this.handleCancel.bind(this)
        });

        ReactDOM.render(dialogContent, this.dialogContainer);
    }

    private handleSave(data: any): void {
        // 处理保存操作
        this.closeDialog(DialogAction.Save, data);
    }

    private handleCancel(): void {
        // 处理取消操作
        this.closeDialog(DialogAction.Cancel);
    }

    private closeDialog(action: DialogAction, data?: any): void {
        // 以操作和可选数据关闭对话框
        powerbi.extensibility.visual.DialogUtils.closeDialog(action, data);
    }
}
```

### 2. 条件格式化集成
```typescript
import powerbiVisualsApi from "powerbi-visuals-api";
import { ColorHelper } from "powerbi-visuals-utils-colorutils";

export class Visual implements IVisual {
    private colorHelper: ColorHelper;

    constructor(options: VisualConstructorOptions) {
        this.colorHelper = new ColorHelper(
            options.host.colorPalette,
            { objectName: "dataPoint", propertyName: "fill" },
            "#3498db"  // 默认颜色
        );
    }

    private applyConditionalFormatting(dataPoints: VisualDataPoint[]): VisualDataPoint[] {
        return dataPoints.map(dataPoint => {
            // 获取条件格式化颜色
            const color = this.colorHelper.getColorForDataPoint(dataPoint.dataViewObject);
            
            return {
                ...dataPoint,
                color: color,
                strokeColor: this.darkenColor(color, 0.2),
                strokeWidth: 2
            };
        });
    }

    private darkenColor(color: string, amount: number): string {
        // 用于为描边变暗的实用函数
        const colorObj = d3.color(color);
        return colorObj ? colorObj.darker(amount).toString() : color;
    }
}
```

### 3. 提示框集成
```typescript
import { createTooltipServiceWrapper, TooltipEventArgs, ITooltipServiceWrapper } from "powerbi-visuals-utils-tooltiputils";

export class Visual implements IVisual {
    private tooltipServiceWrapper: ITooltipServiceWrapper;

    constructor(options: VisualConstructorOptions) {
        this.tooltipServiceWrapper = createTooltipServiceWrapper(
            options.host.tooltipService,
            options.element
        );
    }

    private addTooltips(selection: d3.Selection<any, VisualDataPoint, any, any>): void {
        this.tooltipServiceWrapper.addTooltip(
            selection,
            (tooltipEvent: TooltipEventArgs<VisualDataPoint>) => {
                const dataPoint = tooltipEvent.data;
                return [
                    {
                        displayName: "类别",
                        value: dataPoint.category
                    },
                    {
                        displayName: "值", 
                        value: dataPoint.value.toString()
                    },
                    {
                        displayName: "百分比",
                        value: `${((dataPoint.value / this.totalValue) * 100).toFixed(1)}%`
                    }
                ];
            }
        );
    }
}
```

## 性能优化

### 1. 数据缩减策略
```json
// 带有数据缩减的可视化能力
"dataViewMappings": {
    "categorical": {
        "categories": {
            "for": { "in": "category" },
            "dataReductionAlgorithm": {
                "window": {
                    "count": 300
                }
            }  
        },
        "values": {
            "group": {
                "by": "series",
                "select": [{
                    "for": {
                        "in": "measure"
                    }
                }],
                "dataReductionAlgorithm": {
                    "top": {
                        "count": 100
                    }
                }  
            }
        }
    }
}
```

### 2. 高效渲染模式
```typescript
export class OptimizedVisual implements IVisual {
    private animationFrameId: number;
    private renderQueue: (() => void)[] = [];

    public update(options: VisualUpdateOptions) {
        // 将渲染操作加入队列而非立即执行
        this.queueRender(() => this.performUpdate(options));
    }

    private queueRender(renderFunction: () => void): void {
        this.renderQueue.push(renderFunction);
        
        if (!this.animationFrameId) {
            this.animationFrameId = requestAnimationFrame(() => {
                this.processRenderQueue();
            });
        }
    }

    private processRenderQueue(): void {
        // 处理所有排队的渲染操作
        while (this.renderQueue.length > 0) {
            const renderFunction = this.renderQueue.shift();
            if (renderFunction) {
                renderFunction();
            }
        }
        
        this.animationFrameId = null;
    }

    private performUpdate(options: VisualUpdateOptions): void {
        // 使用虚拟DOM或高效的差异策略
        const currentData = this.transformData(options.dataViews[0]);
        
        if (this.hasDataChanged(currentData)) {
            this.renderVisualization(currentData);
            this.previousData = currentData;
        }
    }

    private hasDataChanged(newData: any[]): boolean {
        // 高效的数据比较
        return JSON.stringify(newData) !== JSON.stringify(this.previousData);
    }
}
```

请记住：自定义可视化开发需要理解Power BI的可视化框架和现代Web开发实践。专注于创建可重用、可测试且高性能的可视化，以增强Power BI生态系统。