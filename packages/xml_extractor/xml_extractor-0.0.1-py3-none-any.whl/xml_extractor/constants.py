version = '0.4.0'
base_filepath = "./"
execution_mode = 'default'
config_filepath = "../config.xacfg"  # default but can be changed (see Main.py)
codification = 'UTF-8'
# extracted from the 'syntax' section of the readme
# todo: change the "how to not write to a file" idea
syntax_help = """
# extracts from file using template
extract from <source_file> using <template_file> to <output_file>
:: <source_file> <template_file> <output_file>  # shortcut for the above
# if <output_file> is exactly None, it will not write to any file and just print the output in the terminal
# example: extract from in.xml using templ1 to out.xml
------------------ in.xml ------------------
<root>
    <b>
        <x>5</x>
        <y>teste</y>
    </b>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
------------------ config.xacfg ------------------
<config>
    <templ1>
        <template>
            <b>
                <y></y>
            </b>
        </template>
        <post_processing>default</post_processing>
    </templ1>
    <templ2>
        <template>
            <tag>another template here</tag>
        </template>
    </templ2>
</config>

(obs.: the chosen template was templ1:
            <b>
                <y></y>
            </b>
------------------ out.xml ------------------
<root>
    <b>
        <y>teste</y>
    </b>
    <b>
        <y>teste2</y>
    </b>
</root>

# filters from <source_file> the occurrences of <candidate> which do not pass the restraining '<field> <comp> <value>'
filter <source_file> to <output_file> keeping <candidate> if <field> <comp> <value>
$ <source_file> <output_file> <candidate> <field> <comp> <value>  # shortcut for the above
    where
        <comp> is the comparison operator operator, which can be ==, =, !=, /=, >, >=, <, <=
# example: filter in.xml to out.xml keeping b if x != 5
------------------ in.xml ------------------
<root>
    <b>
        <x>5</x>
        <y>teste</y>
    </b>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
------------------ out.xml ------------------
<root>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
"""