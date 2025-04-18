% if record.warnings:
    <div class="tooltip-anchor record-warnings">
        % include('components/svg', name='status/warning')
        <div class="tooltip right">
            <div class="title">Potential accidental login</div>
            % for warning in record.warnings:
                <div>{{ warning }}</div>
            % end
        </div>
    </div>
% end
