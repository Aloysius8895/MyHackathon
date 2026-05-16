import {
  Component,
  Input,
  Output,
  OnChanges,
  SimpleChanges,
  EventEmitter,
} from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';
import { CommonModule } from '@angular/common';

interface FieldSchema {
  type: string;
  title: string;
  enum?: string[];
  format?: string;
  description?: string;
}

interface FormSchema {
  type: string;
  title: string;
  description?: string;
  properties: { [key: string]: FieldSchema };
  required?: string[];
}

@Component({
  selector: 'app-forms',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './forms.html',
  styleUrls: ['./forms.css'],
})
export class FormsComponent implements OnChanges {
  @Input() formSchema!: FormSchema;
  @Output() formSubmitted = new EventEmitter<any>();
  form!: FormGroup;
  fieldKeys: string[] = [];
  submitted = false;

  constructor(private fb: FormBuilder) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['formSchema'] && this.formSchema?.properties) {
      this.buildForm();
    }
  }

  buildForm(): void {
    const controlsConfig: { [key: string]: any } = {};
    this.fieldKeys = Object.keys(this.formSchema.properties);

    for (const fieldName of this.fieldKeys) {
      const field = this.formSchema.properties[fieldName];
      const validators = [];

      if (this.formSchema.required?.includes(fieldName)) {
        validators.push(Validators.required);
      }

      if (field.type === 'number') {
        validators.push(Validators.pattern(/^\d+$/));
      }

      controlsConfig[fieldName] = ['', validators];
    }

    this.form = this.fb.group(controlsConfig);
  }

  onSubmit(): void {
    if (this.form.valid) {
      console.log('INSIDE FORM COMPONENT', this.form.value);
      this.submitted = true;
      this.form.disable();
      this.formSubmitted.emit(this.form.value);
    } else {
      console.warn('❌ Form is invalid');
      this.form.markAllAsTouched();
    }
  }
}
