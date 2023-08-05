{{ imports }}
import {connect} from "react-redux";
import axios from "axios";
import {withRouter} from "react-router-dom";
import {PageContextProvider, reloadPageDataAction} from "../../state";{% if streams %}
import {streamEnterAction, streamLeaveAction} from "../../streams";{% endif %}

class {{ name }} extends React.Component {

    setState = (response) => {
        if (response.data.__error__) throw response.data.__error__;
        if (response.data.__state__) {
            this.props.dispatch(reloadPageDataAction(response.data.__state__));
            return response.data.__state__;
        }
        return response.data;
    };
    {% if streams %}
    componentDidMount = () => {
        {% for stream in streams -%}
        this.props.dispatch(
            streamEnterAction(window.location.protocol.replace('http', 'ws') + '//' + window.location.host + '/ws/pages/{{ stream.page.application.app_name }}/{{ stream.page.name }}')
        );
        {%- endfor %}
        this.reload();
    };

    componentWillUnmount() {
        setTimeout(() => {
            {% for stream in streams -%}
            this.props.dispatch(
                streamLeaveAction(window.location.protocol.replace('http', 'ws') + '//' + window.location.host + '/ws/pages/{{ stream.page.application.app_name }}/{{ stream.page.name }}')
            );
            {%- endfor %}
        }, 1000);
    }
    {% else %}
    componentDidMount() {
        this.reload();
    }
    {%- endif %}

    reload = () => axios.get('').then(this.setState);
    {% for name, func in page.list_own_or_parent_functions().items() %}
    {{ name }} = ({% if func.args %}{{ func.render_python_args() }}{% endif %}) => axios.post(window.location.href, {'method': '{{ name }}'{% if func.args %}, args: [{{ func.render_python_args() }}]{% else %}{% endif %}}).then(this.setState);
    {%- endfor %}

    render() {
        return (
            {{ source|indent(12) }}
        );
    }
    {% with blocks=page.get_blocks(platform=ext) %}
    {% if 'content' not in blocks %}
    renderContent = () => <p>Nothing here!</p>;
    {% endif %}
    {% for area, blocks in blocks.items() -%}
    render{{ area|capitalize }} = () => <>{% for block in blocks -%}
        {{ block.render(area=area, index=loop.index)|indent(8) }}
    {% endfor %}</>;
    {% endfor %}
    {% endwith %}
}

{{ name }} = connect(
    store => {
        return {store}
    },
    dispatch => {
        return {dispatch}
    },
)({{ name }});

{{ name }} = withRouter({{ name }});

export default {{ name }};
