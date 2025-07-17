import re

class css:
    def __init__(self, css_text):
        self.css_text = css_text
        self.cleaned_css = self.remove_comments(css_text)
        self.rules = self.parse_rules(self.cleaned_css)
        self.merged = self.merge_rules(self.rules)

    def remove_comments(self, css):
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        css = css.replace("\n", "")
        return css

    def parse_rules(self, css):
        pattern = re.compile(r'([^{]+)\{([^}]+)\}')
        rules = pattern.findall(css)
        return [(selector.strip(), properties.strip()) for selector, properties in rules]

    def merge_properties(self, props1, props2):
        props_dict = {}
        for prop in props1.split(';'):
            if ':' in prop:
                k, v = prop.split(':', 1)
                props_dict[k.strip()] = v.strip()
        for prop in props2.split(';'):
            if ':' in prop:
                k, v = prop.split(':', 1)
                props_dict[k.strip()] = v.strip()
        return '; '.join(f'{k}: {v}' for k, v in props_dict.items() if k) + ';'

    def merge_rules(self, rules):
        merged = {}
        for selector, props in rules:
            if not props.strip():
                continue
            selectors = [s.strip() for s in selector.split(',')]
            for sel in selectors:
                if sel in merged:
                    merged[sel] = self.merge_properties(merged[sel], props)
                else:
                    merged[sel] = props
        return merged

    def get_optimized_css(self):
        return ''.join(f'{selector}{{{props.replace(" ", "")}}}' for selector, props in self.merged.items())
