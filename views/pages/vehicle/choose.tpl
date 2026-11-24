
% rebase('base')

<div id="page-header">
    <h1>Choose a {{ context.format_model_category() }}</h1>
</div>

<p>
    Multiple {{ context.format_model_category(2).lower() }} found with the number {{ vehicle_id }}.
    Please select which {{ context.format_model_category().lower() }} you want to see.
</p>

<table>
    <thead>
        <tr>
            <th>{{ context.format_model_category() }}</th>
            <th class="non-mobile">Model</th>
            <th>Agency</th>
        </tr>
    </thead>
    <tbody>
        % for vehicle in vehicles:
            <tr>
                <td>
                    <div class="column">
                        % include('components/vehicle')
                        <span class="mobile-only smaller-font">
                            % include('components/year_model', year_model=vehicle.year_model)
                        </span>
                    </div>
                </td>
                <td class="non-mobile">
                    % include('components/year_model', year_model=vehicle.year_model)
                </td>
                <td>
                    <div class="row">
                        % include('components/agency_logo', agency=vehicle.agency)
                        {{ vehicle.context }}
                    </div>
                </td>
            </tr>
        % end
    </tbody>
</table>
