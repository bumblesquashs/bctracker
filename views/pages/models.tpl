
% rebase('base')

<div id="page-header">
    <h1>Models</h1>
</div>

% models = sorted({o.model for o in orders})
% model_types = sorted({m.type for m in models})

<div class="page-container">
    <div class="sidebar container flex-1">
        <div class="section">
            <div class="header" onclick="toggleSection(this)">
                <h2>Overview</h2>
                % include('components/toggle')
            </div>
            <div class="content">
                <div class="info-box">
                    <div class="row section">
                        <div class="name">Total</div>
                        <div class="value">{{ sum([o.size for o in orders]) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Seen</div>
                        <div class="value">{{ len(overviews) }}</div>
                    </div>
                    <div class="row section">
                        <div class="name">Tracked</div>
                        <div class="value">{{ len([o for o in overviews.values() if o.last_record]) }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="container flex-3">
        % for model_type in model_types:
            <div class="section">
                <div class="header" onclick="toggleSection(this)">
                    <h2>{{ model_type }}</h2>
                    % include('components/toggle')
                </div>
                <div class="content">
                    <div class="grid start">
                        % type_models = [m for m in models if m.type == model_type]
                        % for model in type_models:
                            % model_orders = [o for o in orders if o.model and o.model == model]
                            % model_overviews = [o for o in overviews.values() if o.bus.model and o.bus.model == model]
                            <div class="info-box">
                                % include('components/photo', photo=None)
                                <div class="column section">
                                    <h3><a href="{{ get_url(system, f'models/{model.id}') }}">{{! model }}</a></h3>
                                    <div class="smaller-font">{{ ', '.join(sorted({ str(o.year) for o in model_orders })) }}</div>
                                </div>
                                <div class="row section space-between">
                                    <div class="column left">
                                        <div class="smaller-font">Total</div>
                                        <div>{{ sum([o.size for o in model_orders]) }}</div>
                                    </div>
                                    <div class="column center">
                                        <div class="smaller-font">Seen</div>
                                        <div>{{ len(model_overviews) }}</div>
                                    </div>
                                    <div class="column right">
                                        <div class="smaller-font">Tracked</div>
                                        <div>{{ len([o for o in model_overviews if o.last_record]) }}</div>
                                    </div>
                                </div>
                            </div>
                        % end
                    </div>
                </div>
            </div>
        % end
    </div>
</div>

% include('components/top_button')
