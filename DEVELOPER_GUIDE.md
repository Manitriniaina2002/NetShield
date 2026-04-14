# NetShield Modern UI - Developer Guide

## 🎯 Component Library Quick Reference

### Overview
All modern UI components are located in `frontend/src/components/ui/`

---

## 📦 Components

### 1. Button Component
**Location**: `ui/button.jsx`

**Variants**: 
- `default` / `primary` - Primary action button
- `secondary` - Secondary action
- `success` - Positive actions
- `outline` - Outlined button
- `destructive` / `danger` - Destructive actions
- `warning` - Warning actions
- `ghost` - Ghost button (transparent)
- `link` - Link-style button

**Sizes**:
- `xs` - Extra small (height: 32px)
- `sm` - Small (height: 36px)
- `default` / `md` - Default (height: 40px, 44px)
- `lg` - Large (height: 48px)
- `xl` - Extra large (height: 56px)
- `icon` / `icon-sm` / `icon-lg` - Icon buttons

**Props**:
```jsx
<Button 
  variant="primary"    // Button style
  size="md"           // Button size
  loading={false}     // Show loading spinner
  disabled={false}    // Disabled state
  onClick={handler}   // Click handler
>
  Click me
</Button>
```

**Examples**:
```jsx
{/* Primary Button */}
<Button variant="primary" size="md">Save Changes</Button>

{/* Loading State */}
<Button loading>Processing...</Button>

{/* Icon Button */}
<Button variant="ghost" size="icon">
  <MenuIcon className="w-5 h-5" />
</Button>

{/* Danger Action */}
<Button variant="danger">Delete</Button>
```

---

### 2. Input Component
**Location**: `ui/input.jsx`

**Props**:
```jsx
<Input 
  type="text"           // Input type
  placeholder="..."     // Placeholder text
  value={value}        // Input value
  onChange={handler}   // Change handler
  error={false}        // Error state
  success={false}      // Success state
  icon={IconComponent} // Icon to display
  iconPosition="left"  // Icon position (left/right)
  disabled={false}     // Disabled state
/>
```

**Examples**:
```jsx
{/* Basic Input */}
<Input placeholder="Enter text" />

{/* Input with Error */}
<Input error placeholder="Invalid input" />

{/* Input with Icon */}
<Input 
  icon={SearchIcon} 
  placeholder="Search..." 
/>

{/* Search Input */}
<Input 
  type="search"
  placeholder="Search networks..."
/>
```

---

### 3. Badge Component
**Location**: `ui/badge.jsx`

**Variants**:
- `default` - Default gray badge
- `primary` - Primary blue badge
- `success` - Success green badge
- `warning` - Warning yellow badge
- `destructive` / `error` - Error red badge
- `info` - Info badge
- `outline` - Outlined badge

**Sizes**:
- `sm` - Small
- `default` - Default
- `lg` - Large

**Props**:
```jsx
<Badge 
  variant="success"
  size="default"
>
  Active
</Badge>
```

**Examples**:
```jsx
{/* Status Badges */}
<Badge variant="success">Online</Badge>
<Badge variant="warning">Pending</Badge>
<Badge variant="destructive">Error</Badge>

{/* Security Badges */}
<Badge variant="success">WPA3</Badge>
<Badge variant="warning">WPA2</Badge>
<Badge variant="destructive">WEP</Badge>

{/* Large Badge */}
<Badge variant="info" size="lg">Important</Badge>
```

---

### 4. Card Component
**Location**: `ui/card.jsx`

**Sub-components**:
- `Card` - Main container
- `CardHeader` - Header section
- `CardTitle` - Title text
- `CardDescription` - Description text
- `CardContent` - Main content area
- `CardFooter` - Footer section

**Props**:
```jsx
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content here</CardContent>
  <CardFooter>Footer content</CardFooter>
</Card>
```

**Examples**:
```jsx
{/* Standard Card */}
<Card>
  <CardHeader>
    <CardTitle>Networks Found</CardTitle>
  </CardHeader>
  <CardContent>
    <p>5 networks detected</p>
  </CardContent>
</Card>

{/* Elevated Card */}
<Card className="card-elevated">
  <CardHeader>Important</CardHeader>
  <CardContent>High priority alert</CardContent>
</Card>
```

---

### 5. Stats Card Component (New)
**Location**: `ui/stats-card.jsx`

**Props**:
```jsx
<StatsCard 
  title="Networks Found"
  value="12"
  subtitle="In last scan"
  icon={NetworkIcon}
  trend={{ up: true, value: 25 }}
  color="primary"  // primary, success, warning, danger, info
  size="default"   // sm, default, lg
/>
```

**Examples**:
```jsx
{/* Basic Stats Card */}
<StatsCard 
  title="Total Devices"
  value="124"
  color="primary"
/>

{/* Card with Trend */}
<StatsCard 
  title="Vulnerabilities"
  value="8"
  subtitle="Critical issues"
  trend={{ up: false, value: 15 }}
  color="danger"
/>

{/* Card with Icon */}
<StatsCard 
  title="Success Rate"
  value="98%"
  icon={CheckIcon}
  color="success"
/>
```

---

### 6. Toast Component (New)
**Location**: `ui/toast.jsx`

**Props**:
```jsx
<Toast 
  message="Action completed"
  type="success"        // success, error, warning, info
  onClose={handler}     // Close callback
  duration={4000}       // Auto-close duration (ms)
  action={{
    label: "Undo",
    onClick: undoHandler
  }}
/>
```

**Examples**:
```jsx
{/* Success Toast */}
<Toast message="Saved successfully" type="success" />

{/* Error Toast */}
<Toast message="Failed to save" type="error" />

{/* Toast with Action */}
<Toast 
  message="Item deleted"
  type="warning"
  action={{ label: "Undo", onClick: undoFn }}
/>
```

---

## 🎨 Color Usage Guide

### Color Variables
```css
/* Primary colors (Blue) */
primary-50 to primary-900

/* Secondary colors (Slate) */
secondary-50 to secondary-900

/* Accent colors (Green) - Success */
accent-50 to accent-900

/* Status colors */
yellow-* (warnings)
red-* (errors/danger)
sky-* (info)
```

### Usage Patterns
```jsx
{/* Success/Positive */}
<Badge variant="success">Active</Badge>
<Button variant="success">Complete</Button>

{/* Warning/Caution */}
<Badge variant="warning">Pending</Badge>
<Button variant="warning">Review</Button>

{/* Error/Danger */}
<Badge variant="destructive">Failed</Badge>
<Button variant="danger">Delete</Button>

{/* Info */}
<Badge variant="info">Notice</Badge>
<Button variant="primary">Learn More</Button>
```

---

## 📏 Spacing Guide

```css
xs:   4px
sm:   8px
md:   16px
lg:   24px
xl:   32px
2xl:  40px
3xl:  48px
```

### Usage
```jsx
{/* Spacing classes */}
<div className="p-4">Padding 16px</div>
<div className="m-6">Margin 24px</div>
<div className="gap-3">Gap 12px between items</div>
<div className="space-y-4">Vertical spacing 16px</div>
```

---

## 🔄 Common Patterns

### Form Layout
```jsx
<div className="space-y-4">
  <div>
    <label className="block text-sm font-medium text-slate-700 mb-2">
      Email
    </label>
    <Input type="email" placeholder="you@example.com" />
  </div>
  <Button variant="primary">Submit</Button>
</div>
```

### Action Group
```jsx
<div className="flex gap-3">
  <Button variant="primary">Save</Button>
  <Button variant="secondary">Cancel</Button>
  <Button variant="ghost">Help</Button>
</div>
```

### Stats Section
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  <StatsCard title="Total" value="100" />
  <StatsCard title="Active" value="75" color="success" />
  <StatsCard title="Pending" value="20" color="warning" />
  <StatsCard title="Failed" value="5" color="danger" />
</div>
```

### Responsive Grid
```jsx
{/* Responsive: 1 col mobile, 2 cols tablet, 3 cols desktop */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map(item => (
    <Card key={item.id}>
      {/* content */}
    </Card>
  ))}
</div>
```

---

## 🎯 Best Practices

### 1. **Consistent Spacing**
Use the spacing scale consistently:
```jsx
<Card className="p-6">                    {/* 24px padding */}
  <h2 className="text-2xl mb-4">Title</h2>  {/* 16px bottom margin */}
  <div className="space-y-3">              {/* 12px between items */}
    {items}
  </div>
</Card>
```

### 2. **Color Semantics**
Use colors to convey meaning:
```jsx
{/* Use semantic colors */}
<Badge variant="success">Secure</Badge>
<Badge variant="warning">Risk</Badge>
<Badge variant="danger">Critical</Badge>
```

### 3. **Button Hierarchy**
Use button variants to show importance:
```jsx
{/* Primary actions first, secondary alternatives */}
<Button variant="primary">Save</Button>
<Button variant="secondary">Cancel</Button>
```

### 4. **Responsive Design**
Test on all breakpoints:
```jsx
<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
  {/* Automatically responsive */}
</div>
```

### 5. **Loading States**
Show progress during actions:
```jsx
<Button variant="primary" loading>
  Processing...
</Button>
```

---

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### Responsive Classes
```jsx
{/* Classes for different screen sizes */}
<div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
  {/* Full width on mobile, half on tablet, etc */}
</div>

<div className="flex flex-col md:flex-row gap-4">
  {/* Stack on mobile, row on tablet+ */}
</div>

<div className="text-sm md:text-base lg:text-lg">
  {/* Text size changes with screen */}
</div>
```

---

## 🚀 Performance Tips

1. **Use CSS classes** instead of inline styles when possible
2. **Lazy load** heavy components
3. **Memoize** callback functions in lists
4. **Use key** prop correctly in mapped lists
5. **Optimize** re-renders with proper state management

---

## 🔗 Related Files
- Global styles: `src/index.css`
- Design tokens: `tailwind.config.js`
- Component registry: `src/components/ui/`

---

**Last Updated**: April 2026
**Version**: 1.0.0 (Modern UI)
