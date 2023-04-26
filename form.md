### Introduction
YAML (short for "YAML Ain't Markup Language") is a human-readable data serialization language that is commonly used for configuration files. 

In the context of form creation, YAML is used to define the structure and contents of the form. In this documentation, we will cover the basics of creating a form using YAML.

### Creating a new section
A section is a group of related widgets in a form. To add a new section to your form, you can create a new YAML block with the `section` key. Here's an example:

```yaml
- section:
    title: Section Title
    widgets:
      - ...
      - ...
```

In this example, the `title` key is used to set the title of the section, and the `widgets` key is used to define the widgets in the section.

### Adding widgets to a section
A widget is an element in a form that the user can interact with. To add a widget to a section, you can create a new YAML block with the `type` key. Here's an example:

```yaml
- section:
    title: Section Title
    widgets:
      - type: entry
        label_text: Widget Label
      - type: dropdown
        label_text: Widget Label
        options:
          - Option 1
          - Option 2
          - Option 3
        multi_select: false
        Tags: false
      - type: text
        label_text: Widget Label
```

In this example, we have added three different types of widgets: an `entry` widget, a `dropdown` widget, and a `text` widget. Each widget has a `label_text` key, which is used to set the label of the widget.

### Working with the dropdown widget
The `dropdown` widget is used to present a list of options to the user, and allow the user to select one or more options from the list. In the example above, we have used the `options` key to define the list of options.

The `multi_select` key is used to indicate whether the user is allowed to select multiple options from the list. If `multi_select` is set to `true`, the user can select multiple options. If it is set to `false`, the user can only select one option.

The `Tags` key is used to enable or disable tags feature. If set to `true`, the user can add new tags to the dropdown list.

If the widget type is dropdown, the parameters `multi_select` and `Tags` are required.

### Adding different types of widgets

Each widget is defined using a dictionary that contains the following keys:

- type: specifies the type of the widget, e.g. entry, dropdown, or text.
- label_text: specifies the label text for the widget, i.e. the text that appears next to the widget to describe what it is.
- options: specifies the list of options for a dropdown widget. For example, the "Project name" dropdown has a list of options.
- multi_select: specifies whether the user can select multiple options in a dropdown. If set to true, the user can select multiple options. If set to false, the user can only select one option.
- tags: specifies whether tags can be added to a dropdown. If set to true, tags can be added. If set to false, tags cannot be added.